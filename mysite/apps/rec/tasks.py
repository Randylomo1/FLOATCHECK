from celery import shared_task
from .models import Reconciliation, InternalRecord, ExternalRecord, Discrepancy

@shared_task
def run_reconciliation(reconciliation_id):
    try:
        reconciliation = Reconciliation.objects.get(id=reconciliation_id)
        reconciliation.status = 'in_progress'
        reconciliation.save()

        internal_records = InternalRecord.objects.filter(reconciliation=reconciliation)
        external_records = ExternalRecord.objects.filter(reconciliation=reconciliation)

        # Simple reconciliation logic (to be improved)
        internal_ids = {record.transaction_id for record in internal_records}
        external_ids = {record.transaction_id for record in external_records}

        missing_in_internal = external_ids - internal_ids
        missing_in_external = internal_ids - external_ids

        for transaction_id in missing_in_internal:
            external_record = ExternalRecord.objects.get(reconciliation=reconciliation, transaction_id=transaction_id)
            Discrepancy.objects.create(
                reconciliation=reconciliation,
                type='missing_in_internal',
                external_record=external_record,
                details=f"Transaction ID {transaction_id} found in external records but not in internal records."
            )

        for transaction_id in missing_in_external:
            internal_record = InternalRecord.objects.get(reconciliation=reconciliation, transaction_id=transaction_id)
            Discrepancy.objects.create(
                reconciliation=reconciliation,
                type='missing_in_external',
                internal_record=internal_record,
                details=f"Transaction ID {transaction_id} found in internal records but not in external records."
            )

        # Check for amount mismatches
        for internal_record in internal_records:
            try:
                external_record = ExternalRecord.objects.get(
                    reconciliation=reconciliation,
                    transaction_id=internal_record.transaction_id
                )
                if internal_record.amount != external_record.amount:
                    Discrepancy.objects.create(
                        reconciliation=reconciliation,
                        type='amount_mismatch',
                        internal_record=internal_record,
                        external_record=external_record,
                        details=f"Amount mismatch for transaction ID {internal_record.transaction_id}: internal amount {internal_record.amount}, external amount {external_record.amount}"
                    )
            except ExternalRecord.DoesNotExist:
                pass  # Already handled as missing_in_external

        reconciliation.status = 'completed'
        reconciliation.save()

    except Reconciliation.DoesNotExist:
        # Handle case where reconciliation is not found
        pass
    except Exception as e:
        # Handle other exceptions and possibly mark the reconciliation as failed
        reconciliation.status = 'failed'
        reconciliation.save()
