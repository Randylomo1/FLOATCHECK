import requests
from requests.auth import HTTPBasicAuth
import json
from django.conf import settings
from datetime import datetime
import base64

def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    try:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        r.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        # Handle connection errors or bad responses
        return None, str(e)

    try:
        mpesa_access_token = r.json()
        return mpesa_access_token.get("access_token"), None
    except json.JSONDecodeError:
        # Handle cases where the response is not valid JSON
        return None, "Invalid JSON response"

def lipa_na_mpesa(phone_number, amount):
    access_token, error = get_mpesa_access_token()
    if error:
        return None, error

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}

    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = settings.MPESA_PASSKEY
    business_short_code = settings.MPESA_BUSINESS_SHORT_CODE

    data_to_encode = f"{business_short_code}{passkey}{lipa_time}"
    online_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": online_password,
        "Timestamp": lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Randy molo",
        "TransactionDesc": "Web Development Charges"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)
