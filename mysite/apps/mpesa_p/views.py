from django.shortcuts import render
from django.contrib import messages
from .lipa_na_mpesa import lipa_na_mpesa
import re

def format_phone_number(phone_number):
    # Remove all non-digit characters
    phone_number = re.sub(r'\D', '', phone_number)
    # Check if the number starts with 254
    if phone_number.startswith('254'):
        return phone_number
    # If it starts with a 0, replace with 254
    if phone_number.startswith('0'):
        return '254' + phone_number[1:]
    # If it starts with 7, assume it's a Kenyan number and prepend 254
    if phone_number.startswith('7'):
        return '254' + phone_number
    # Otherwise, return the number as is, which will likely fail validation
    return phone_number

def lipa_na_mpesa_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')

        if not phone_number or not amount:
            messages.error(request, 'Phone number and amount are required.')
            return render(request, 'mpesa_p/pay.html')

        try:
            # For simplicity, we'll cast to int. In a real app, use Decimal.
            valid_amount = int(amount)
            if valid_amount < 1:
                raise ValueError("Amount must be a positive number.")
        except ValueError:
            messages.error(request, 'Invalid amount. Please enter a valid number.')
            return render(request, 'mpesa_p/pay.html')

        formatted_phone_number = format_phone_number(phone_number)

        response, error = lipa_na_mpesa(formatted_phone_number, str(valid_amount))

        if error:
            messages.error(request, f"Error: {error}")
        else:
            messages.success(request, f"Success: {response.get('ResponseDescription')}")

        return render(request, 'mpesa_p/pay.html')

    return render(request, 'mpesa_p/pay.html')

def mpesa_callback_view(request):
    # This view will be implemented in a future step.
    return render(request, 'mpesa_p/callback.html')

def pay(request):
    return render(request, 'mpesa_p/pay.html')
