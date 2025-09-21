from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Reconciliation, Discrepancy, InternalRecord, ExternalRecord
from apps.business.models import Business
from .tasks import run_reconciliation
from .forms import CSVUploadForm
import csv

@login_required
def create_reconciliation(request):
    business = get_object_or_404(Business, user=request.user)
    Reconciliation.objects.create(business=business)
    messages.success(request, "New reconciliation created.")
    return HttpResponseRedirect(reverse('rec:reconciliation_list'))

@login_required
def reconciliation_list(request):
    reconciliations = Reconciliation.objects.filter(business__user=request.user)

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
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['csv_path'] = form.cleaned_data['file'].temporary_file_path()
            return redirect('rec:map_columns', reconciliation_id=reconciliation.id, record_type=record_type)
    else:
        form = CSVUploadForm()
    return render(request, 'rec/upload_records.html', {
        'form': form,
        'reconciliation': reconciliation,
        'record_type': record_type
    })

@login_required
def map_columns(request, reconciliation_id, record_type):
    reconciliation = get_object_or_404(Reconciliation, id=reconciliation_id, business__user=request.user)
    csv_path = request.session.get('csv_path')
    if not csv_path:
        messages.error(request, "No CSV file found.")
        return redirect('rec:reconciliation_detail', reconciliation_id=reconciliation.id)

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

    if request.method == 'POST':
        mapping = {
            'transaction_id': request.POST['transaction_id'],
            'amount': request.POST['amount'],
            'date': request.POST['date'],
        }

        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            if record_type == 'internal':
                InternalRecord.objects.filter(reconciliation=reconciliation).delete()
                for row in reader:
                    InternalRecord.objects.create(
                        reconciliation=reconciliation,
                        transaction_id=row[mapping['transaction_id']],
                        amount=row[mapping['amount']],
                        date=row[mapping['date']]
                    )
            elif record_type == 'external':
                ExternalRecord.objects.filter(reconciliation=reconciliation).delete()
                for row in reader:
                    ExternalRecord.objects.create(
                        reconciliation=reconciliation,
                        transaction_id=row[mapping['transaction_id']],
                        amount=row[mapping['amount']],
                        date=row[mapping['date']]
                    )

        del request.session['csv_path']
        messages.success(request, f"{record_type.capitalize()} records uploaded successfully.")
        return redirect('rec:reconciliation_detail', reconciliation_id=reconciliation.id)

    return render(request, 'rec/map_columns.html', {
        'reconciliation': reconciliation,
        'record_type': record_type,
        'header': header
    })