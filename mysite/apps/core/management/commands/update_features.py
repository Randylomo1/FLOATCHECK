from django.core.management.base import BaseCommand
from apps.core.models import Feature

class Command(BaseCommand):
    help = 'Updates the features in the database to reflect the current application functionality.'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing features...')
        Feature.objects.all().delete()

        self.stdout.write('Creating new features...')
        # Core Features
        Feature.objects.create(name='User Authentication', description='Secure login, logout, and user registration.', icon='users')
        Feature.objects.create(name='Business Management', description='Create and manage your business profile.', icon='briefcase')
        Feature.objects.create(name='Dashboard', description='A central hub for a quick overview of your financial activities.', icon='tachometer-alt')

        # Payment Processing
        Feature.objects.create(name='M-Pesa Integration', description='Seamlessly process payments with M-Pesa.', icon='credit-card')
        Feature.objects.create(name='File-Based Payment Ingestion', description='Upload payment records in various formats, including CSV, Excel, and PDF.', icon='file-upload')

        # Reconciliation
        Feature.objects.create(name='Automated Reconciliation', description='Automatically match transactions with invoices.', icon='cogs')
        Feature.objects.create(name='Reconciliation Rule Builder', description='Create custom rules for matching transactions.', icon='ruler-combined')
        Feature.objects.create(name='Exception Queue', description='Manage and review transactions that require manual attention.', icon='filter')
        Feature.objects.create(name='Manual Matching', description='Manually match transactions to invoices with ease.', icon='hand-pointer')
        Feature.objects.create(name='Bulk Actions', description='Perform actions on multiple transactions at once.', icon='tasks')
        Feature.objects.create(name='Export Reconciliation Results', description='Export your reconciliation data for reporting and analysis.', icon='file-export')

        # Auditing
        Feature.objects.create(name='Audit Logging', description='Track user actions for security and compliance.', icon='history')

        self.stdout.write(self.style.SUCCESS('Successfully updated the features in the database.'))
