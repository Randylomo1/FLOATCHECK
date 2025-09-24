# mysite/check_creds_standalone.py
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Assuming the .env file is in the parent directory of 'mysite'
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

consumer_key = os.getenv('MPESA_CONSUMER_KEY')
consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
params = {'grant_type': 'client_credentials'}

print("--- Standalone M-Pesa Credential Check ---")
if not consumer_key or not consumer_secret:
    print("ERROR: M-Pesa consumer key or secret is not configured in your .env file.")
else:
    print(f"Consumer Key Loaded: {'Yes' if consumer_key else 'No'}")
    print(f"Consumer Secret Loaded: {'Yes' if consumer_secret else 'No'}")
    print("------------------------------------")
    try:
        print(f"Attempting to get access token from: {api_URL}")
        r = requests.get(api_URL, params=params, auth=HTTPBasicAuth(consumer_key, consumer_secret), timeout=30)
        r.raise_for_status()
        access_token = r.json()["access_token"]
        print(f"SUCCESS: Successfully obtained access token: {access_token}")
    except requests.exceptions.RequestException as e:
        print(f"FAILED: Failed to get access token: {e}")
        if e.response is not None:
            print(f"FAILED: Response Status Code: {e.response.status_code}")
            print(f"FAILED: Response Body: {e.response.text}")
