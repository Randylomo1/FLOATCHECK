# This file will contain service functions for ingesting data from various external APIs.
# By centralizing this logic, we can easily add new ingestion sources in the future.

from .models import PaymentSource, Transaction


def ingest_from_bank_api(payment_source: PaymentSource):
    """
    Placeholder service to fetch and ingest transactions from a partner bank's API.

    This function will be responsible for:
    1. Authenticating with the bank's API using credentials stored in the PaymentSource.
    2. Fetching the latest transactions since the last sync.
    3. Transforming the bank's data format into our internal Transaction model.
    4. Saving the new transactions to the database.
    """
    print(f"INFO: Ingesting from bank API for source: {payment_source.name} - NOT IMPLEMENTED")
    # TODO: Implement the actual logic to connect to the bank API.
    pass

def ingest_from_mpesa_api(payment_source: PaymentSource):
    """
    Placeholder service to fetch and ingest transactions from the M-Pesa G2 API.

    This function will be responsible for:
    1. Authenticating with the M-Pesa API.
    2. Querying for new transactions.
    3. Handling the callback from the M-Pesa API if required.
    4. Transforming the data into our internal Transaction model.
    5. Saving the new transactions to the database.
    """
    print(f"INFO: Ingesting from M-Pesa API for source: {payment_source.name} - NOT IMPLEMENTED")
    # TODO: Implement the actual logic to connect to the M-Pesa G2 API.
    pass

def run_ingestion_for_source(payment_source_id: int):
    """
    Dispatches the ingestion task to the correct service based on the source type.
    This would typically be called from a Celery task.
    """
    try:
        payment_source = PaymentSource.objects.get(id=payment_source_id)
        
        if payment_source.source_type == 'bank_api':
            ingest_from_bank_api(payment_source)
        elif payment_source.source_type == 'mpesa_api':
            ingest_from_mpesa_api(payment_source)
        else:
            print(f"WARNING: No ingestion service found for source type: {payment_source.source_type}")

    except PaymentSource.DoesNotExist:
        print(f"ERROR: PaymentSource with id {payment_source_id} not found.")
