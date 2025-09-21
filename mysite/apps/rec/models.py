from django.db import models
from apps.business.models import Business

class Reconciliation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reconciliations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_status_badge_class(self):
        return {
            'pending': 'bg-secondary',
            'in_progress': 'bg-primary',
            'completed': 'bg-success',
            'failed': 'bg-danger',
        }.get(self.status, 'bg-dark')

    def __str__(self):
        return f"Reconciliation {self.id} for {self.business.name}"

class InternalRecord(models.Model):
    reconciliation = models.ForeignKey(Reconciliation, on_delete=models.CASCADE, related_name='internal_records')
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f"Internal Record {self.transaction_id}"

class ExternalRecord(models.Model):
    reconciliation = models.ForeignKey(Reconciliation, on_delete=models.CASCADE, related_name='external_records')
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f"External Record {self.transaction_id}"

class Discrepancy(models.Model):
    DISCREPANCY_CHOICES = (
        ('missing_in_internal', 'Missing in Internal'),
        ('missing_in_external', 'Missing in External'),
        ('amount_mismatch', 'Amount Mismatch'),
    )
    reconciliation = models.ForeignKey(Reconciliation, on_delete=models.CASCADE, related_name='discrepancies')
    type = models.CharField(max_length=50, choices=DISCREPANCY_CHOICES)
    internal_record = models.ForeignKey(InternalRecord, on_delete=models.CASCADE, null=True, blank=True)
    external_record = models.ForeignKey(ExternalRecord, on_delete=models.CASCADE, null=True, blank=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Discrepancy {self.id} for Reconciliation {self.reconciliation.id}"
