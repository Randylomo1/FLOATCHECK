from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from weasyprint import HTML
from .models import Reconciliation, InternalRecord, ExternalRecord, Discrepancy, ReconciliationRule, TransactionException

@shared_task
def send_scheduled_report(reconciliation_id, recipient_email):
    """
    Generates a reconciliation report and emails it to the specified recipient.
    """
    try:
        reconciliation = Reconciliation.objects.get(id=reconciliation_id)
        discrepancies = Discrepancy.objects.filter(reconciliation=reconciliation)
        business = reconciliation.business

        html_string = render_to_string('rec/reconciliation_report.html', {
            'reconciliation': reconciliation,
            'discrepancies': discrepancies,
            'business': business
        })

        html = HTML(string=html_string)
        pdf = html.write_pdf()

        subject = f"Reconciliation Report for {business.name}"
        body = "Please find attached the reconciliation report."
        email = EmailMessage(
            subject,
            body,
            'noreply@floatcheck.com',
            [recipient_email]
        )
        email.attach(f'reconciliation_report_{reconciliation_id}.pdf', pdf, 'application/pdf')
        email.send()

    except Reconciliation.DoesNotExist:
        print(f"Reconciliation with ID {reconciliation_id} does not exist.")
    except Exception as e:
        print(f"An error occurred while sending the scheduled report for reconciliation ID {reconciliation_id}: {e}")

@shared_task
def run_reconciliation(reconciliation_id):
    try:
        reconciliation = Reconciliation.objects.get(id=reconciliation_id)
        reconciliation.status = 'in_progress'
        reconciliation.save()

        internal_records = list(InternalRecord.objects.filter(reconciliation=reconciliation))
        external_records = list(ExternalRecord.objects.filter(reconciliation=reconciliation))
        rules = ReconciliationRule.objects.filter(business=reconciliation.business)

        matched_internal_indices = set()
        matched_external_indices = set()

        # Apply rules first
        for rule in rules:
            for i, internal_record in enumerate(internal_records):
                if i in matched_internal_indices:
                    continue
                for j, external_record in enumerate(external_records):
                    if j in matched_external_indices:
                        continue

                    is_match = False
                    if rule.field_to_match == 'amount':
                        if internal_record.amount == external_record.amount:
                            is_match = True
                    elif rule.field_to_match == 'transaction_id':
                        if rule.match_type == 'exact' and internal_record.transaction_id == external_record.transaction_id:
                            is_match = True
                        elif rule.match_type == 'contains' and rule.value in internal_record.transaction_id:
                            is_match = True
                        elif rule.match_type == 'startswith' and internal_record.transaction_id.startswith(rule.value):
                            is_match = True

                    if is_match:
                        Discrepancy.objects.create(
                            reconciliation=reconciliation,
                            internal_record=internal_record,
                            external_record=external_record,
                            reason=f"Matched by rule: {rule.name}"
                        )
                        matched_internal_indices.add(i)
                        matched_external_indices.add(j)
                        break  # Move to the next internal record

        # Handle unmatched records by creating exceptions
        for i, record in enumerate(internal_records):
            if i not in matched_internal_indices:
                TransactionException.objects.create(
                    reconciliation=reconciliation,
                    transaction_id=record.transaction_id,
                    amount=record.amount,
                    date=record.date,
                    source='internal',
                    description='No matching external record found.'
                )

        for i, record in enumerate(external_records):
            if i not in matched_external_indices:
                TransactionException.objects.create(
                    reconciliation=reconciliation,
                    transaction_id=record.transaction_id,
                    amount=record.amount,
                    date=record.date,
                    source='external',
                    description='No matching internal record found.'
                )

        reconciliation.status = 'completed'
        reconciliation.save()

    except Reconciliation.DoesNotExist:
        # Log the error appropriately
        print(f"Reconciliation with ID {reconciliation_id} does not exist.")
    except Exception as e:
        # Log the exception
        print(f"An error occurred during reconciliation for ID {reconciliation_id}: {e}")
        try:
            reconciliation = Reconciliation.objects.get(id=reconciliation_id)
            reconciliation.status = 'failed'
            reconciliation.save()
        except Reconciliation.DoesNotExist:
            pass # Already handled
