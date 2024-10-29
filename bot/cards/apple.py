import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from db import get_user_by_username
from .passbook.passbook.models import *

CARDS_DIR = "wallet_cards"
SAVE_PATH_FOR_CARDS = Path(__file__).parent.parent / CARDS_DIR
load_dotenv()


def generate_apple_wallet_card(
    name: str,
    username: str,
) -> None:
    user = get_user_by_username(username)
    
    if not user:
        return

    user_id = user.id

    cardInfo = Coupon()
    cardInfo.addSecondaryField('', name, 'Имя')
    cardInfo.addSecondaryField('', user_id, 'Номер')
    cardInfo.addHeaderField('статус карты', 'ПРЕМИУМ', 'статус карты')

    for field in cardInfo.secondaryFields:
        field.textAlignment = Alignment.CENTER

    organizationName = 'MOSCOW CARD TM' 
    passTypeIdentifier = os.getenv("APPLE_TYPE_IDENTIFIER", None) 
    teamIdentifier = os.getenv("APPLE_TEAM_IDENTIFIER", None)

    passfile = Pass(cardInfo, \
        passTypeIdentifier=passTypeIdentifier, \
        organizationName=organizationName, \
        teamIdentifier=teamIdentifier)

    passfile.backgroundColor = '#FF3040'
    passfile.foregroundColor = '#FFFFFF'
    passfile.labelColor = '#FFFFFF'

    # Including the icon and logo is necessary for the passbook to be valid.
    passfile.addFile('strip.png', open('./cards/images/background.png', 'rb'))
    passfile.addFile('logo.png', open('./cards/images/logo.png', 'rb'))
    passfile.addFile('icon.png', open('./cards/images/icon.png', 'rb'))

    save_path = SAVE_PATH_FOR_CARDS / f'{username}.pkpass'

    passfile.create('./cards/keys_certs/pass.pem', 
                    './cards/keys_certs/private.key', 
                    './cards/keys_certs/AppleWWDRCA.pem', 
                    None, save_path)

