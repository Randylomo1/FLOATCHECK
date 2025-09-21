from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class PaymentSource(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Business(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_businesses')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='staff')

    def __str__(self):
        return f'{self.user.username} - {self.business.name}'

class SubscriptionPlan(models.Model):
    TIER_CHOICES = (
        ('free', 'Free'),
        ('standard', 'Standard'),
        ('professional', 'Professional'),
    )
    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=dict)

    def __str__(self):
        return self.name

class BusinessSubscription(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.business.name} - {self.plan.name if self.plan else "No Plan"}'

class PaymentLink(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    payment_link_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Payment link for {self.business.name} - {self.amount}'
