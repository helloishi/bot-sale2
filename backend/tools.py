import re
import os
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

CLOUD_PAYMENTS_BASE_URL = "https://api.cloudpayments.ru"
CLOUD_PAYMENTS_FETCH_SUBS = f"{CLOUD_PAYMENTS_BASE_URL}/subscriptions/find"
CLOUD_PAYMENTS_STOP_SUB_LINK = f"{CLOUD_PAYMENTS_BASE_URL}/subscriptions/cancel"
TELEGRAM_LINK_REGEX = r't\.me\/(\w+)'

load_dotenv()

def validate_username(username: str) -> str:
    username = username.replace("@", "")
    match = re.match(r't\.me\/(\w+)', username)
    
    if match:
        username = match.group(1)

    return username.lower()

def fetch_payments_from_cloud_payments(email: str) -> Optional[list[str]]:
    if not email: 
        return

    payload = {
        "accountId": email
    }

    login, password = os.getenv("PAYMENT_API_ID"), os.getenv("PAYMENT_API_PASS")

    response = requests.post(
        CLOUD_PAYMENTS_FETCH_SUBS, 
        data=payload,
        auth=HTTPBasicAuth(login, password)
    )

    response = response.json()

    if not response:
        return

    ids = []

    if response["Success"] == True and response["Model"]:
        for sub in response["Model"]:
            sub_id = sub.get("Id", None)

            if sub_id:
                ids.append(sub_id)

    return ids


def stop_cloud_payments_recurrent(ids: list[str], email:str) -> None:
    if not ids:
        return

    for id_ in ids:
        payload = {
            "subscriptionId": id_,
            "AccountId": email,
        } 

        login, password = os.getenv("PAYMENT_API_ID"), os.getenv("PAYMENT_API_PASS")

        response = requests.post(
            CLOUD_PAYMENTS_FETCH_SUBS, 
            data=payload,
            auth=HTTPBasicAuth(login, password)
        )

        response = response.json()

        print(response)

        if response["Success"]:
            print(f"Subscription {id_} successfully stopped!")
