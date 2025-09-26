
from django.test import TestCase
from .models import Reconciliation, InternalRecord, ExternalRecord, Discrepancy
from business.models import Business
from django.contrib.auth import get_user_model

User = get_user_model()

class ReconciliationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.business = Business.objects.create(
            name='Test Business',
            user=self.user,
            industry='IT',
            phone_number='1234567890',
            contact_email='business@example.com'
        )
        self.reconciliation = Reconciliation.objects.create(
            business=self.business,
            status='pending'
        )

    def test_reconciliation_creation(self):
        self.assertEqual(Reconciliation.objects.count(), 1)
        self.assertEqual(self.reconciliation.business, self.business)
        self.assertEqual(self.reconciliation.status, 'pending')

    def test_reconciliation_str(self):
        self.assertEqual(str(self.reconciliation), f"Reconciliation #{self.reconciliation.id} for {self.business.name}")

    def test_get_status_badge_class(self):
        self.assertEqual(self.reconciliation.get_status_badge_class(), 'bg-secondary')
        self.reconciliation.status = 'completed'
        self.reconciliation.save()
        self.assertEqual(self.reconciliation.get_status_badge_class(), 'bg-success')
