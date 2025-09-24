from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import IntegrationForm
from .models import Integration
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# New imports for the API
from rest_framework import viewsets
from .models import Customer, Product, Invoice, InvoiceItem, Payment
from .serializers import (
    CustomerSerializer,
    ProductSerializer,
    InvoiceSerializer,
    InvoiceItemSerializer,
    PaymentSerializer,
)

@login_required
def integration_list(request):
    """View to list all active integrations for the current user."""
    integrations = Integration.objects.filter(user=request.user)
    return render(request, 'integrations/integration_list.html', {'integrations': integrations})

@login_required
def connect_integration(request):
    """View to handle the connection of a new integration."""
    if request.method == 'POST':
        form = IntegrationForm(request.POST, user=request.user)
        if form.is_valid():
            integration = form.save(commit=False)
            integration.user = request.user
            integration.is_active = True  # Mark as active upon successful connection
            integration.save()
            # Here, you would typically redirect to the ERP's authorization page
            # and handle the OAuth2 callback.
            # For this example, we'll just redirect to the integration list.
            return redirect('integrations:integration_list')
    else:
        form = IntegrationForm(user=request.user)
    return render(request, 'integrations/connect_integration.html', {'form': form})


@csrf_exempt
def webhook_receiver(request):
    """
    Handles incoming webhooks from external services.
    """
    if request.method == 'POST':
        # In a real application, you would verify the webhook signature here
        # to ensure it's from a trusted source.
        payload = json.loads(request.body)
        
        # Process the webhook payload
        # This could involve creating, updating, or deleting data in your application
        # based on the event that triggered the webhook.
        print(f"Received webhook: {payload}")
        
        # Return a 200 OK response to acknowledge receipt of the webhook.
        return HttpResponse(status=200)
    
    # Return a 405 Method Not Allowed if the request is not a POST.
    return HttpResponse(status=405)

# API Viewsets

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # Add permissions and filtering by business/user

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Add permissions and filtering by business/user

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows invoices to be viewed or edited.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    # Add permissions and filtering by business/user

class InvoiceItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows invoice items to be viewed or edited.
    """
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
    # Add permissions and filtering by business/user

class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows payments to be viewed or edited.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    # Add permissions and filtering by business/user
