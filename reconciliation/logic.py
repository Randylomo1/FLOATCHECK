from payments.models import Transaction, Invoice, Reconciliation, MatchingRule
from django.db.models import Q
from datetime import timedelta
from thefuzz import fuzz

def find_best_match_for_transaction(transaction, invoices):
    """
    Finds the best invoice match for a single transaction from a list of invoices.
    Returns the best matching invoice and the confidence score.
    """
    best_match = None
    highest_score = 0

    for invoice in invoices:
        score = 0
        explanations = []

        # Rule 1: Exact Amount Match (High Importance)
        if transaction.amount == invoice.amount_due:
            score += 60
            explanations.append("Exact amount match.")

        # Rule 2: Time Window Match (Medium Importance)
        # Match if the transaction happened within 3 days of the invoice due date.
        if abs((transaction.timestamp.date() - invoice.due_date)) <= timedelta(days=3):
            score += 15
            explanations.append("Transaction date is close to invoice due date.")

        # Rule 3: Fuzzy Name/Info Matching (Medium Importance)
        # Compare invoice customer name with transaction payer info.
        if transaction.payer_info:
            ratio = fuzz.token_set_ratio(invoice.customer_name, transaction.payer_info)
            if ratio > 80: # High similarity threshold
                score += 25
                explanations.append(f"Payer info is {ratio}% similar to customer name.")

        # Rule 4: Reference ID Match (Bonus)
        # Look for the invoice number within the transaction reference or payer info.
        if transaction.reference_id and invoice.invoice_number in transaction.reference_id:
            score += 30 # Give a significant bonus for this
            explanations.append("Invoice number found in transaction reference.")
        elif transaction.payer_info and invoice.invoice_number in transaction.payer_info:
            score += 20
            explanations.append("Invoice number found in payer info.")

        if score > highest_score:
            highest_score = score
            best_match = invoice
    
    # Normalize to 100 if score exceeds it
    highest_score = min(highest_score, 100)

    return best_match, highest_score, explanations

def run_matching_engine():
    """
    Core logic for the automatic reconciliation engine.
    Matches unmatched transactions with unpaid invoices using a rule-based scoring system.
    """
    # Fetch all necessary data in bulk to reduce DB queries
    unmatched_transactions = list(Transaction.objects.filter(status='unmatched'))
    unpaid_invoices = list(Invoice.objects.filter(status='unpaid'))
    
    if not unmatched_transactions or not unpaid_invoices:
        print("No transactions or invoices to match.")
        return

    matches_made = 0
    exceptions_found = 0
    CONFIDENCE_THRESHOLD = 85 # We need a high confidence to auto-match

    for transaction in unmatched_transactions:
        # For a given transaction, find the best possible invoice match
        best_invoice, score, explanations = find_best_match_for_transaction(transaction, unpaid_invoices)

        if best_invoice and score >= CONFIDENCE_THRESHOLD:
            # Create a Reconciliation record for the match
            Reconciliation.objects.create(
                transaction=transaction,
                invoice=best_invoice,
                confidence_score=score,
                status='auto',
                # We can add a field to store the `explanations` later if needed
            )

            # Update the status of both records
            transaction.status = 'matched'
            transaction.save()

            best_invoice.status = 'paid'
            best_invoice.save()
            
            # Remove the matched invoice from the pool to avoid double-matching
            unpaid_invoices.remove(best_invoice)
            matches_made += 1
        else:
            # If no confident match is found, mark the transaction as an exception
            transaction.status = 'exception'
            transaction.save()
            exceptions_found += 1
    
    print(f"Matching complete. Matches made: {matches_made}. Exceptions: {exceptions_found}.")
