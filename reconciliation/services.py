# reconciliation/services.py

from payments.models import Transaction, Payment
from .models import Reconciliation

def reconcile_transactions_and_payments():
    # Get all unreconciled transactions and payments
    unreconciled_transactions = Transaction.objects.filter(reconciliation__isnull=True)
    unreconciled_payments = Payment.objects.filter(reconciliation__isnull=True)

    for transaction in unreconciled_transactions:
        for payment in unreconciled_payments:
            # Basic matching logic: amount and near timestamp
            if (transaction.amount == payment.amount and 
                abs(transaction.timestamp - payment.timestamp).total_seconds() < 3600):

                # Create a new Reconciliation object
                reconciliation = Reconciliation.objects.create(
                    transaction=transaction,
                    payment=payment,
                    status='matched'
                )
                # Update the reconciliation ID
                reconciliation.reconciliation_id = f"rec_{reconciliation.id}"
                reconciliation.save()

                # Break the inner loop since we found a match
                break
