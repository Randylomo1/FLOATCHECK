from django.core.management.base import BaseCommand
from apps.core.models import Feature, PricingPlan

class Command(BaseCommand):
    help = 'Populates the database with initial data for Features and Pricing Plans.'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        Feature.objects.all().delete()
        PricingPlan.objects.all().delete()

        self.stdout.write('Creating new features...')
        feature1 = Feature.objects.create(name='Real-time Monitoring', description='Monitor your finances in real-time with our intuitive dashboard.', icon='clock')
        feature2 = Feature.objects.create(name='Expense Tracking', description='Keep track of your expenses and categorize them for better financial insights.', icon='chart-pie')
        feature3 = Feature.objects.create(name='Budgeting Tools', description='Create and manage budgets to stay on top of your financial goals.', icon='wallet')
        feature4 = Feature.objects.create(name='Automated Reporting', description='Generate automated reports to get a clear overview of your financial health.', icon='file-alt')
        feature5 = Feature.objects.create(name='AI-Powered Insights', description='Get personalized insights and recommendations powered by our advanced AI.', icon='robot')
        feature6 = Feature.objects.create(name='Secure & Encrypted', description='Your data is safe and secure with our bank-level encryption.', icon='shield-alt')

        self.stdout.write('Creating new pricing plans...')
        plan1 = PricingPlan.objects.create(name='Basic', price=0.00)
        plan1.features.add(feature1, feature2)

        plan2 = PricingPlan.objects.create(name='Pro', price=14.99)
        plan2.features.add(feature1, feature2, feature3, feature4)

        plan3 = PricingPlan.objects.create(name='Enterprise', price=49.99)
        plan3.features.add(feature1, feature2, feature3, feature4, feature5, feature6)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with initial data.'))
