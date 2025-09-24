from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from ..models import User

def verify_email(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
    except User.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return redirect('login')

    if user.email_verified:
        messages.info(request, "Your email has already been verified.")
    else:
        user.email_verified = True
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been verified successfully!")

    # Log the user in
    login(request, user)

    return redirect('dashboard')
