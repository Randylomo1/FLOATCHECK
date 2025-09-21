import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from payments.models import Transaction, MatchingRule, Invoice, AuditLog, Business
from .forms import MatchingRuleForm
from django.utils import timezone

class ExceptionQueueView(View):
    def get(self, request):
        exceptions = Transaction.objects.filter(status='exception')
        return render(request, 'reconciliation/exception_queue.html', {'exceptions': exceptions})

class RuleBuilderView(View):
    def get(self, request):
        form = MatchingRuleForm()
        rules = MatchingRule.objects.all()
        return render(request, 'reconciliation/rule_builder.html', {'form': form, 'rules': rules})

    def post(self, request):
        form = MatchingRuleForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            try:
                # Validate and pretty-print the JSON
                logic_dict = json.loads(rule.logic)
                rule.logic = json.dumps(logic_dict, indent=4)
            except json.JSONDecodeError:
                form.add_error('logic', 'Invalid JSON format.')
                rules = MatchingRule.objects.all()
                return render(request, 'reconciliation/rule_builder.html', {'form': form, 'rules': rules})

            business = Business.objects.first()
            if not business:
                pass 
            rule.business = business

            rule.save()
            messages.success(request, 'New matching rule created successfully.')
            return redirect('reconciliation:rule_builder')
        
        rules = MatchingRule.objects.all()
        return render(request, 'reconciliation/rule_builder.html', {'form': form, 'rules': rules})

class ManualMatchView(View):
    def get(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        suggested_invoices = Invoice.objects.filter(
            business=transaction.business, 
            amount_due=transaction.amount, 
            status='unpaid'
        )
        
        return render(request, 'reconciliation/manual_match.html', {
            'transaction': transaction,
            'suggested_invoices': suggested_invoices
        })

    def post(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        invoice_id = request.POST.get('invoice_id')

        if invoice_id:
            invoice = get_object_or_404(Invoice, id=invoice_id)

            transaction.status = 'matched'
            transaction.invoice = invoice
            transaction.matched_at = timezone.now()
            transaction.save()

            invoice.status = 'paid'
            invoice.save()

            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=f"Manually matched Transaction #{transaction.id} to Invoice #{invoice.id}",
                details=f"Transaction with amount {transaction.amount} was matched to Invoice with amount {invoice.amount_due}."
            )
            
            messages.success(request, f"Transaction #{transaction.id} matched successfully to Invoice #{invoice.id}.")
            return redirect('reconciliation:exception_queue')
        else:
            messages.warning(request, 'No invoice selected.')
            return redirect('reconciliation:manual_match', transaction_id=transaction_id)

class BulkActionView(View):
    def post(self, request):
        action = request.POST.get('action')
        transaction_ids = request.POST.getlist('transaction_ids')

        if not transaction_ids:
            messages.info(request, "No transactions selected.")
            return redirect('reconciliation:exception_queue')

        if action == 'dismiss':
            transactions = Transaction.objects.filter(id__in=transaction_ids)
            count = transactions.update(status='dismissed', matched_at=timezone.now())

            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=f"Bulk dismissed {count} transactions.",
                details=f"Transaction IDs: {', '.join(transaction_ids)}"
            )
            messages.success(request, f"{count} transactions have been dismissed.")
        
        elif action == 'match':
            matched_count = 0
            for transaction_id in transaction_ids:
                transaction = get_object_or_404(Transaction, id=transaction_id)
                
                potential_invoices = Invoice.objects.filter(
                    business=transaction.business,
                    amount_due=transaction.amount,
                    status='unpaid'
                )
                
                if potential_invoices.count() == 1:
                    invoice = potential_invoices.first()
                    
                    transaction.status = 'matched'
                    transaction.invoice = invoice
                    transaction.matched_at = timezone.now()
                    transaction.save()
                    
                    invoice.status = 'paid'
                    invoice.save()
                    
                    matched_count += 1

            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=f"Attempted bulk matching for {len(transaction_ids)} transactions.",
                details=f"Successfully matched {matched_count} transactions."
            )
            messages.success(request, f"Attempted to match {len(transaction_ids)} transactions. Successfully matched {matched_count}.")

        return redirect('reconciliation:exception_queue')
