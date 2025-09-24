from django.contrib import admin
from .models import DataRetentionPolicy


@admin.register(DataRetentionPolicy)
class DataRetentionPolicyAdmin(admin.ModelAdmin):
    """
    Admin interface for the DataRetentionPolicy model.
    """
    list_display = ('name', 'content_type', 'retention_period_days', 'is_active', 'created_at')
    list_filter = ('is_active', 'content_type')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
