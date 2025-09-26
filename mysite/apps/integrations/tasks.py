
from celery import shared_task
from .models import Webhook
from business.models import Business
from payments.models import Transaction, PaymentSource
from django.utils import timezone

@shared_task
def process_webhook(webhook_id):
    """
    Process an incoming webhook from an ERP system.
    """
    try:
        webhook = Webhook.objects.get(id=webhook_id)
    except Webhook.DoesNotExist:
        return f"Webhook {webhook_id} not found."

    integration = webhook.integration
    user = integration.user

    try:
        business = Business.objects.get(owner=user)
    except Business.DoesNotExist:
        return f"Business not found for user {user.id}"

    payload = webhook.payload
    transaction_id = payload.get('transaction_id')
    amount = payload.get('amount')
    # Assuming the ERP payload includes a 'source' identifier
    source_name = payload.get('source', integration.get_integration_type_display())
    

    # Get or create the PaymentSource
    source, _ = PaymentSource.objects.get_or_create(name=source_name)

    if transaction_id and amount:
        # Create a new Transaction
        Transaction.objects.create(
            business=business,
            source=source,
            transaction_id=transaction_id,
            amount=amount,
            timestamp=webhook.received_at, # Or a timestamp from the payload
            status='pending'
        )
        return f"Transaction {transaction_id} created successfully."
    else:
        return f"Webhook {webhook_id} did not contain transaction_id or amount."
