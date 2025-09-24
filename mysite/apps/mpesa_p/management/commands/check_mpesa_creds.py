
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth

class Command(BaseCommand):
    help = "Check M-Pesa credentials and get an access token"

    def handle(self, *args, **options):
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        # URL without query parameters
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
        # Parameters as a dictionary
        params = {'grant_type': 'client_credentials'}

        self.stdout.write("--- M-Pesa Credential Diagnostic (v2) ---")

        if not consumer_key or not consumer_secret:
            self.stderr.write(self.style.ERROR("M-Pesa consumer key or secret is not configured in your .env file."))
            return

        self.stdout.write(f"Consumer Key (type: {type(consumer_key)}, length: {len(consumer_key)}): '{consumer_key}'")
        self.stdout.write(f"Consumer Secret (type: {type(consumer_secret)}, length: {len(consumer_secret)}): '{consumer_secret}'")
        self.stdout.write("------------------------------------")

        try:
            self.stdout.write(f"Attempting to get access token from: {api_URL}")
            self.stdout.write(f"With params: {params}")
            # Pass the URL and the params separately
            r = requests.get(api_URL, params=params, auth=HTTPBasicAuth(consumer_key, consumer_secret), timeout=30)
            r.raise_for_status()  # Raise an exception for bad status codes
            access_token = r.json()["access_token"]
            self.stdout.write(self.style.SUCCESS(f"Successfully obtained access token: {access_token}"))
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Failed to get access token: {e}"))
            if e.response is not None:
                self.stderr.write(self.style.ERROR(f"Response Status Code: {e.response.status_code}"))
                self.stderr.write(self.style.ERROR(f"Response Body: {e.response.text}"))
