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
        self.encoded_secret = base64.b64encode(self.api_secret.encode()).decode()

        print(self.public_id, self.api_secret)

    def create_payment(self, amount, currency, invoice_id, description, account_id, card_cryptogram_packet):
        url = f"{self.base_url}payments/cards/topup"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.encoded_secret}'
        }

        data = {
            "Amount": float(amount),
            "Currency": currency,
            "CardCryptogramPacket": card_cryptogram_packet
        }

        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code in (200, 201):
            return response.json()

        return {}
