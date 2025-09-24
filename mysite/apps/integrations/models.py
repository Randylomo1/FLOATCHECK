from django.db import models
from django.contrib.auth import get_user_model
from encrypted_model_fields.fields import EncryptedCharField
from ..business.models import Business

User = get_user_model()

class Integration(models.Model):
    """
    Represents a connection to an external accounting or ERP system.
    """
    class IntegrationType(models.TextChoices):
        QUICKBOOKS = 'quickbooks', 'QuickBooks'
        XERO = 'xero', 'Xero'
        SAGE = 'sage', 'Sage'
        # Add other ERPs as needed

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='integrations')
    integration_type = models.CharField(
        max_length=50,
        choices=IntegrationType.choices,
        verbose_name='Integration Type'
    )
    is_active = models.BooleanField(default=False, verbose_name='Is Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # In a real application, these credentials should be stored securely.
    # Consider using django-encrypted-model-fields or a dedicated secrets manager.
    api_key = EncryptedCharField(max_length=255, blank=True, null=True, help_text="Store securely!")
    api_secret = EncryptedCharField(max_length=255, blank=True, null=True, help_text="Store securely!")

    class Meta:
        unique_together = ('user', 'integration_type')
        verbose_name = 'Integration'
        verbose_name_plural = 'Integrations'

    def __str__(self):
        return f"{self.get_integration_type_display()} for {self.user.email}"


class Webhook(models.Model):
    """
    Represents a webhook received from an external system.
    """
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='webhooks')
    received_at = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField()

    def __str__(self):
        return f"Webhook for {self.integration} at {self.received_at}"

# Start of new models for the Universal ERP Hub

class Customer(models.Model):
    """
    Represents a customer, which can be an individual or a company.
    This is the canonical representation of a customer within FloatCheck.
    """
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID from the external ERP system")
    integration = models.ForeignKey(Integration, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Represents a product or service offered by the business.
    This is the canonical representation of a product within FloatCheck.
    """
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID from the external ERP system")
    integration = models.ForeignKey(Integration, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name

class Invoice(models.Model):
    """
    Represents an invoice issued to a customer.
    This is the canonical representation of an invoice within FloatCheck.
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('void', 'Void'),
    )

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='invoices')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=255)
    issue_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID from the external ERP system")
    integration = models.ForeignKey(Integration, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.customer}"

class InvoiceItem(models.Model):
    """
    Represents a line item on an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} on {self.invoice.invoice_number}"

class Payment(models.Model):
    """
    Represents a payment made towards an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID from the external ERP system")
    integration = models.ForeignKey(Integration, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.invoice.invoice_number}"
