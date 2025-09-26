from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.urls import reverse
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Reconciliation, Discrepancy, InternalRecord, ExternalRecord, ColumnMappingTemplate, ReconciliationRule, TransactionException, ScheduledReport
from business.models import Business
from .tasks import run_reconciliation
from .forms import FileUploadForm # Updated form name
from . import parsers
import os
from django.utils import timezone
from datetime import timedelta

@login_required
def create_reconciliation(request):
    business = get_object_or_404(Business, user=request.user)
    Reconciliation.objects.create(business=business)
    messages.success(request, "New reconciliation created.")
    return HttpResponseRedirect(reverse('rec:reconciliation_list'))

@login_required
def reconciliation_list(request):
    reconciliations = Reconciliation.objects.filter(business__user=request.user)
    # ... (rest of the view is unchanged)
    search_id = request.GET.get('search_id')
    if search_id:
        reconciliations = reconciliations.filter(id=search_id)

    status = request.GET.get('status')
    if status:
        reconciliations = reconciliations.filter(status=status)

    start_date = request.GET.get('start_date')
    if start_date:
        reconciliations = reconciliations.filter(created_at__gte=start_date)

    end_date = request.GET.get('end_date')
    if end_date:
        reconciliations = reconciliations.filter(created_at__lte=end_date)

    return render(request, 'rec/reconciliation_list.html', {'reconciliations': reconciliations})

@login_required
def run_reconciliation_view(request, reconciliation_id):
    reconciliation = get_object_or_404(Reconciliation, id=reconciliation_id, business__user=request.user)
    run_reconciliation.delay(reconciliation.id)
    messages.info(request, f"Reconciliation #{reconciliation.id} has been started.")
    return HttpResponseRedirect(reverse('rec:reconciliation_list'))

@login_required
def reconciliation_detail(request, reconciliation_id):
    reconciliation = get_object_or_404(Reconciliation, id=reconciliation_id, business__user=request.user)
    discrepancies = Discrepancy.objects.filter(reconciliation=reconciliation)
    return render(request, 'rec/reconciliation_detail.html', {
        'reconciliation': reconciliation,
        'discrepancies': discrepancies
    })

@login_required
def download_reconciliation_report(request, reconciliation_id):
    reconciliation = get_object_or_404(Reconciliation, id=reconciliation_id, business__user=request.user)
    discrepancies = Discrepancy.objects.filter(reconciliation=reconciliation)
    business = reconciliation.business

    html_string = render_to_string('rec/reconciliation_report.html', {
        'reconciliation': reconciliation,
        'discrepancies': discrepancies,
        'business': business
    })

    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reconciliation_report_{reconciliation_id}.pdf"'
    return response

@login_required
def schedule_report(request, reconciliation_id):
    reconciliation = get_object_or_404(Reconciliation, id=reconciliation_id, business__user=request.user)
    scheduled_reports = ScheduledReport.objects.filter(reconciliation=reconciliation)

    if request.method == 'POST':
        frequency = request.POST.get('frequency')
        recipient_email = request.POST.get('recipient_email')

        if frequency and recipient_email:
            now = timezone.now()
            next_run_at = now
            if frequency == 'daily':
                next_run_at += timedelta(days=1)
            elif frequency == 'weekly':
                next_run_at += timedelta(weeks=1)
            elif frequency == 'monthly':
                next_run_at += timedelta(days=30)

            ScheduledReport.objects.create(
                reconciliation=reconciliation,
                frequency=frequency,
                recipient_email=recipient_email,
                next_run_at=next_run_at
            )
            messages.success(request, 'Report scheduled successfully.')
            return redirect('rec:schedule_report', reconciliation_id=reconciliation.id)
        else:
            messages.error(request, 'Please provide both frequency and recipient email.')

    return render(request, 'rec/schedule_report.html', {
        'reconciliation': reconciliation,
        'scheduled_reports': scheduled_reports
    })

@login_required
def delete_scheduled_report(request, report_id):
    report = get_object_or_404(ScheduledReport, id=report_id, reconciliation__business__user=request.user)
    reconciliation_id = report.reconciliation.id
    report.delete()
    messages.success(request, "Scheduled report deleted successfully.")
    return redirect('rec:schedule_report', reconciliation_id=reconciliation_id)

@login_required
def delete_reconciliation(request, reconciliation_id):
    reconciliation = get_object_or_404(Reconciliation, id=reconciliation_id, business__user=request.user)
    if reconciliation.status == 'pending':
        reconciliation.delete()
        messages.success(request, f"Reconciliation #{reconciliation.id} has been deleted.")
    else:
        messages.error(request, "Only pending reconciliations can be deleted.")
    return redirect('rec:reconciliation_list')

@login_required
def upload_records(request, reconciliation_id, record_type):
    reconciliation = get_object_or_404(Reconciliation, id=reconciliation_id, business__user=request.user)
    business = get_object_or_404(Business, user=request.user)
    templates = ColumnMappingTemplate.objects.filter(business=business)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            temp_path = default_storage.save(f"tmp/{uploaded_file.name}", ContentFile(uploaded_file.read()))
            
            parser_map = {
                '.csv': parsers.parse_csv,
                '.xlsx': parsers.parse_excel,
                '.xls': parsers.parse_excel,
                '.pdf': parsers.parse_pdf,
                '.ofx': parsers.parse_ofx,
            }
            parser_func = parser_map.get(file_ext)

            if not parser_func:
                default_storage.delete(temp_path)
                messages.error(request, f"Unsupported file type: {file_ext}. Please upload a CSV, Excel, PDF, or OFX file.")
                return redirect('rec:upload_records', reconciliation_id=reconciliation.id, record_type=record_type)

            try:
                header, data = parser_func(temp_path)
                request.session['file_header'] = header
                request.session['file_data'] = data
                request.session['template_id'] = request.POST.get('template')
                return redirect('rec:map_columns', reconciliation_id=reconciliation.id, record_type=record_type)
            except Exception as e:
                messages.error(request, f"Failed to parse file. It may be corrupted or in an unexpected format. Error: {e}")
            finally:
                if default_storage.exists(temp_path):
                    default_storage.delete(temp_path)
        else:
            messages.error(request, "No file was uploaded or the form is invalid. Please try again.")

    form = FileUploadForm()
    return render(request, 'rec/upload_records.html', {
        'form': form,
        'reconciliation': reconciliation,
        'record_type': record_type,
        'templates': templates
    })

@login_required
def map_columns(request, reconciliation_id, record_type):
    reconciliation = get_object_or_404(Reconciliation, id=reconciliation_id, business__user=request.user)
    header = request.session.get('file_header')
    data = request.session.get('file_data')

    if not header or data is None:
        messages.error(request, "No file data found in session. Please upload the file again.")
        return redirect('rec:upload_records', reconciliation_id=reconciliation.id, record_type=record_type)

    mapping = None
    template_id = request.session.pop('template_id', None)
    if template_id:
        mapping = get_object_or_404(ColumnMappingTemplate, id=template_id, business=reconciliation.business)

    if request.method == 'POST':
        submitted_mapping = {
            'transaction_id': request.POST.get('transaction_id'),
            'amount': request.POST.get('amount'),
            'date': request.POST.get('date'),
        }

        if 'save_template' in request.POST:
            template_name = request.POST.get('template_name')
            if template_name and all(submitted_mapping.values()):
                ColumnMappingTemplate.objects.create(
                    business=reconciliation.business,
                    name=template_name,
                    transaction_id_column=submitted_mapping['transaction_id'],
                    amount_column=submitted_mapping['amount'],
                    date_column=submitted_mapping['date'],
                )
                messages.success(request, f"Template '{template_name}' saved successfully.")
            else:
                messages.error(request, "To save a template, you must provide a name and map all required fields.")
            # Re-render the page to show success/error message for template saving
            return render(request, 'rec/map_columns.html', {
                'reconciliation': reconciliation,
                'record_type': record_type,
                'header': header,
                'mapping': {
                    'transaction_id_column': submitted_mapping['transaction_id'],
                    'amount_column': submitted_mapping['amount'],
                    'date_column': submitted_mapping['date']
                }
            })

        elif 'import_data' in request.POST:
            if not all(submitted_mapping.values()):
                messages.error(request, "Please map all required fields before importing.")
            else:
                try:
                    RecordModel = InternalRecord if record_type == 'internal' else ExternalRecord
                    RecordModel.objects.filter(reconciliation=reconciliation).delete()

                    id_index = header.index(submitted_mapping['transaction_id'])
                    amount_index = header.index(submitted_mapping['amount'])
                    date_index = header.index(submitted_mapping['date'])

                    records_to_create = []
                    for row in data:
                        records_to_create.append(RecordModel(
                            reconciliation=reconciliation,
                            transaction_id=row[id_index],
                            amount=row[amount_index],
                            date=row[date_index]
                        ))
                    RecordModel.objects.bulk_create(records_to_create)

                    messages.success(request, f"{len(records_to_create)} {record_type.capitalize()} records imported successfully.")
                    request.session.pop('file_header', None)
                    request.session.pop('file_data', None)
                    return redirect('rec:reconciliation_detail', reconciliation_id=reconciliation.id)
                except (ValueError, IndexError) as e:
                    messages.error(request, f"A mismatch occurred between the mapping and the file data. Please re-check your column selections. Error: {e}")
                except Exception as e:
                    messages.error(request, f"An unexpected error occurred during import: {e}")

    return render(request, 'rec/map_columns.html', {
        'reconciliation': reconciliation,
        'record_type': record_type,
        'header': header,
        'mapping': mapping
    })

@login_required
def rule_builder(request):
    business = get_object_or_404(Business, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        field_to_match = request.POST.get('field_to_match')
        match_type = request.POST.get('match_type')
        value = request.POST.get('value')

        if name and field_to_match and match_type and value:
            ReconciliationRule.objects.create(
                business=business,
                name=name,
                field_to_match=field_to_match,
                match_type=match_type,
                value=value
            )
            messages.success(request, f"Rule '{name}' created successfully.")
            return redirect('rec:rule_builder')
        else:
            messages.error(request, "Please fill in all fields to create a rule.")

    rules = ReconciliationRule.objects.filter(business=business)
    return render(request, 'rec/rule_builder.html', {'rules': rules})

@login_required
def delete_rule(request, rule_id):
    rule = get_object_or_404(ReconciliationRule, id=rule_id, business__user=request.user)
    rule.delete()
    messages.success(request, "Rule deleted successfully.")
    return redirect('rec:rule_builder')


@login_required
def exception_queue(request):
    business = get_object_or_404(Business, user=request.user)
    exceptions = TransactionException.objects.filter(reconciliation__business=business)

    reconciliation_id = request.GET.get('reconciliation_id')
    if reconciliation_id:
        exceptions = exceptions.filter(reconciliation_id=reconciliation_id)

    return render(request, 'rec/exception_queue.html', {'exceptions': exceptions})
