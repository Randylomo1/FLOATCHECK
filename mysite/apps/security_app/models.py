from django.db import models
from django.contrib.contenttypes.models import ContentType

class DataRetentionPolicy(models.Model):
    """
    A policy for retaining data for a certain period of time.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    retention_period_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
