from django.contrib import admin
from .models import (
    Integration,
    Webhook,
    Customer,
    Product,
    Invoice,
    InvoiceItem,
    Payment,
)

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    readonly_fields = ('total_price',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('integration_type', 'user', 'is_active', 'created_at')
    list_filter = ('integration_type', 'is_active')
    search_fields = ('user__email',)

@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ('id', 'integration', 'received_at')
    list_filter = ('integration',)
    readonly_fields = ('received_at', 'payload')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'email', 'phone', 'external_id')
    search_fields = ('name', 'email', 'business__name')
    list_filter = ('business',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'price', 'external_id')
    search_fields = ('name', 'business__name')
    list_filter = ('business',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'business', 'issue_date', 'due_date', 'total_amount', 'status')
    search_fields = ('invoice_number', 'customer__name', 'business__name')
    list_filter = ('status', 'business', 'issue_date', 'due_date')
    inlines = [InvoiceItemInline, PaymentInline]
    readonly_fields = ('created_at', 'updated_at')

# The following models are managed via inlines in the InvoiceAdmin,
# so they don't need a separate registration unless direct management is desired.
# admin.site.register(InvoiceItem)
# admin.site.register(Payment)
