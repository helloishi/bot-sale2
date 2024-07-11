import os

import requests
import base64
from dotenv import load_dotenv

load_dotenv()

class CloudPayments:
    def __init__(self, public_id, api_secret):
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

        
        if response.status_code in (200, 201):
            return response.json()

        return {}
