
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ContactForm
from .models import Feature, PricingPlan, User
from apps.business.models import Business
from apps.rec.models import Reconciliation, InternalRecord, ExternalRecord, Discrepancy

def splash(request):
    return render(request, 'splash.html')

def landing(request):
    return render(request, 'landing.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()  # Refresh the user object from the database

            # Send verification email
            token = user.email_verification_token
            verification_link = request.build_absolute_uri(reverse('core:verify_email', args=[token]))
            subject = 'Verify your email address'
            message = f'Please click the following link to verify your email address: {verification_link}'
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                reply_to=['molorandyc4@gmail.com'],
            )
            email.send()

            return render(request, 'registration/verification_sent.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def verify_email(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
    except User.DoesNotExist:
        return render(request, 'registration/invalid_token.html')

    user.is_active = True
    user.email_verified = True
    user.email_verification_token = None
    user.save()
    login(request, user)
    return redirect('core:dashboard')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('core:splash')

@login_required
def dashboard(request):
    try:
        business = request.user.business
    except Business.DoesNotExist:
        return redirect('business:business_setup')

    # Financial Summary
    reconciliations = Reconciliation.objects.filter(business=business)
    total_reconciliations = reconciliations.count()
    completed_reconciliations = reconciliations.filter(status='completed').count()
    total_discrepancies = Discrepancy.objects.filter(reconciliation__in=reconciliations).count()

    # Recent Transactions (using Internal Records as an example)
    recent_transactions = InternalRecord.objects.filter(reconciliation__business=business).order_by('-date')[:5]

    # Chart Data
    chart_labels = ['Completed', 'Pending', 'In Progress', 'Failed']
    chart_data = [
        reconciliations.filter(status='completed').count(),
        reconciliations.filter(status='pending').count(),
        reconciliations.filter(status='in_progress').count(),
        reconciliations.filter(status='failed').count()
    ]

    context = {
        'total_reconciliations': total_reconciliations,
        'completed_reconciliations': completed_reconciliations,
        'total_discrepancies': total_discrepancies,
        'recent_transactions': recent_transactions,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html')

def features(request):
    features = Feature.objects.all()
    return render(request, 'features.html', {'features': features})

def pricing(request):
    pricing_plans = PricingPlan.objects.all()
    return render(request, 'pricing.html', {'pricing_plans': pricing_plans})

def about(request):
    return render(request, 'about.html')

def contact(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(f'Name: {form.cleaned_data["name"]}\nEmail: {form.cleaned_data["email"]}\nMessage: {form.cleaned_data["message"]}')
            success = True
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'success': success})
