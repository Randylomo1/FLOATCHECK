from django.shortcuts import render
from django.contrib import messages
from . import lipa_na_mpesa

def home(request):
    return render(request, 'home.html', {'navbar': 'home'})

def token(request):
    access_token, error = lipa_na_mpesa.get_mpesa_access_token()
    if error:
        messages.error(request, f"Error getting access token: {error}")
        return render(request, 'token.html')

    return render(request, 'token.html', {"token": access_token})

def pay(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')

        if not phone or not amount:
            messages.error(request, "Phone number and amount are required.")
            return render(request, 'pay.html', {'navbar': 'stk'})

        response, error = lipa_na_mpesa.lipa_na_mpesa(phone, amount)

        if error:
            messages.error(request, f"Error processing payment: {error}")
        elif response and response.get("ResponseCode") == "0":
            messages.success(request, "Payment request sent successfully!")
        else:
            messages.warning(request, f"Payment request failed: {response.get('ResponseDescription') if response else 'Unknown error'}")

    return render(request, 'pay.html', {'navbar': 'stk'})

def stk(request):
    return render(request, 'pay.html', {'navbar': 'stk'})
