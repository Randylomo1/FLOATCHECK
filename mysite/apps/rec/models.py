from django.db import models
from business.models import Business

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

    def __str__(self):
        return f"Reconciliation #{self.id} for {self.business.name}"

    def get_status_badge_class(self):
        return {
            'pending': 'bg-secondary',
            'in_progress': 'bg-info',
            'completed': 'bg-success',
            'failed': 'bg-danger',
        }.get(self.status, 'bg-dark')

class InternalRecord(models.Model):
    reconciliation = models.ForeignKey(Reconciliation, on_delete=models.CASCADE, related_name='internal_records')
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class ExternalRecord(models.Model):
    reconciliation = models.ForeignKey(Reconciliation, on_delete=models.CASCADE, related_name='external_records')
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class Discrepancy(models.Model):
    reconciliation = models.ForeignKey(Reconciliation, on_delete=models.CASCADE, related_name='discrepancies')
    internal_record = models.OneToOneField(InternalRecord, on_delete=models.CASCADE, null=True, blank=True)
    external_record = models.OneToOneField(ExternalRecord, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.CharField(max_length=255, default='', blank=True)

class ColumnMappingTemplate(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='column_mapping_templates')
    name = models.CharField(max_length=100)
    transaction_id_column = models.CharField(max_length=100)
    amount_column = models.CharField(max_length=100)
    date_column = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ReconciliationRule(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='rules')
    name = models.CharField(max_length=100)
    field_to_match = models.CharField(max_length=100)  # e.g., 'amount', 'transaction_id'
    match_type = models.CharField(max_length=50)  # e.g., 'exact', 'contains', 'startswith'
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TransactionException(models.Model):
    reconciliation = models.ForeignKey(Reconciliation, on_delete=models.CASCADE, related_name='exceptions')
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=20)  # 'internal' or 'external'

    def __str__(self):
        return f"Exception for Reconciliation #{self.reconciliation.id} - {self.transaction_id}"

class ScheduledReport(models.Model):
    reconciliation = models.ForeignKey(Reconciliation, on_delete=models.CASCADE, related_name='scheduled_reports')
    frequency = models.CharField(max_length=20, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])
    recipient_email = models.EmailField()
    next_run_at = models.DateTimeField()

    def __str__(self):
        return f"Scheduled report for Reconciliation #{self.reconciliation.id}"
