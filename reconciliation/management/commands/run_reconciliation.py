from django.core.management.base import BaseCommand
from reconciliation.logic import run_matching_engine

class Command(BaseCommand):
    help = 'Runs the reconciliation matching engine'

    def handle(self, *args, **options):
        self.stdout.write('Starting reconciliation...')
        run_matching_engine()
        self.stdout.write(self.style.SUCCESS('Reconciliation complete!'))
