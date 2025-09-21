# reconciliation/management/commands/reconcile.py

from django.core.management.base import BaseCommand
from reconciliation.services import reconcile_transactions_and_payments

class Command(BaseCommand):
    help = 'Reconciles transactions and payments'

    def handle(self, *args, **options):
        self.stdout.write('Starting reconciliation...')
        reconcile_transactions_and_payments()
        self.stdout.write(self.style.SUCCESS('Reconciliation complete.'))
