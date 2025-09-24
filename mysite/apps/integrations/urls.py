from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    integration_list,
    connect_integration,
    webhook_receiver,
    CustomerViewSet,
    ProductViewSet,
    InvoiceViewSet,
    InvoiceItemViewSet,
    PaymentViewSet,
)

app_name = 'integrations'

# API Router
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'invoice-items', InvoiceItemViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', integration_list, name='integration_list'),
    path('connect/', connect_integration, name='connect_integration'),
    path('webhook/', webhook_receiver, name='webhook_receiver'),

    # API Endpoints
    path('api/', include(router.urls)),
]
