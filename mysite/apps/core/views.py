from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ContactForm
from .models import Feature, PricingPlan
from apps.business.models import Business

def splash(request):
    return render(request, 'splash.html')

def landing(request):
    return render(request, 'landing.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('business_setup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('splash')

@login_required
def dashboard(request):
    try:
        business = request.user.business
    except Business.DoesNotExist:
        return redirect('business_setup')
    return render(request, 'dashboard.html')

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
