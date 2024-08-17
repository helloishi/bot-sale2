import os
import uuid
import json 

from yookassa import Payment, Configuration
from dotenv import load_dotenv

load_dotenv()

Configuration.account_id = os.getenv("YOOKASSA_ACCOUNT_ID")
Configuration.secret_key = os.getenv("YOOKASSA_KEY")

SUBSCRIPTION_COST = 299

class YooKassaPayment:
    @staticmethod
    def get_confirmation_token() -> str:
        payment = Payment.create({
            "amount": {
                "value": f"{SUBSCRIPTION_COST}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "embedded"
            },
            "capture": True,
            "description": "Оплата подписки в moscowcard.ru"
        })

        payment = payment.json()
        payment = json.loads(payment)

        return payment["confirmation"]["confirmation_token"]

    @staticmethod
    def get_confirmation_link() -> str:
        payment = Payment.create({
            "amount": {
                "value": f"{SUBSCRIPTION_COST}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://moscowcard.ru/thank-you"
            },
            "capture": True,
            "description": "Заказ №1"
        })

        payment = payment.json()
        payment = json.loads(payment)

        return payment["confirmation"]["confirmation_url"]