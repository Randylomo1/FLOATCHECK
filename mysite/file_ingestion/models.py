from django.db import models

class FinancialDocument(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=10)
    processing_status = models.CharField(max_length=20, default='pending')

class Transaction(models.Model):
    document = models.ForeignKey(FinancialDocument, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
