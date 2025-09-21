from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='check-circle')

    def __str__(self):
        return self.name

class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField(Feature)

    def __str__(self):
        return self.name
