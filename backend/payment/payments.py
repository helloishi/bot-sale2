import os

import requests
import base64
from dotenv import load_dotenv

from django.http import HttpResponseRedirect
from rest_framework import status

load_dotenv()

class CloudPayments:
    def __init__(self):
        self.public_id = os.environ.get("PAYMENT_API_ID")
        self.api_secret = os.environ.get("PAYMENT_API_PASS")
        self.base_url = "https://api.cloudpayments.ru/"

    def create_payment(self, amount, currency, invoice_id, description, account_id, card_cryptogram_packet):
        url = f"{self.base_url}payments/cards/charge"

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "Amount": float(amount),
            "Currency": currency,
            "CardCryptogramPacket": card_cryptogram_packet
        }

        response = requests.post(url, 
                            json=data, 
                            headers=headers, 
                            auth=requests.auth.HTTPBasicAuth(self.public_id, self.api_secret))

        
        if not 'application/json' in response.headers.get('Content-Type', ''):
            return {"error": "Couldn't fetch the data from payment"}, status.HTTP_400_BAD_REQUEST

        response_data = response.json()
        model = response_data.get("Model", {})

        if model.get("PaReq") and model.get("AcsUrl"):
            pa_req = model.get("PaReq")
            acs_url = model.get("AcsUrl")

            _3ds_request = requests.post(acs_url, json={
                "PaReq": pa_req, 
                "MD": model.get("TransactionId") 
            })

            return _3ds_request, status.HTTP_200_OK

        if response_data.get("Success"):
            return response_data, status.HTTP_200_OK

        return response_data, status.HTTP_400_BAD_REQUEST