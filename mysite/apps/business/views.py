from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Business
from .forms import BusinessForm

@login_required
def business_setup(request):
    try:
        business = request.user.business
    except Business.DoesNotExist:
        business = None

    if request.method == 'POST':
        form = BusinessForm(request.POST, instance=business)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.save()
            return redirect('dashboard')
    else:
        form = BusinessForm(instance=business)

    return render(request, 'business/business_setup.html', {'form': form})
