import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from db import get_user_by_username
from .passbook.passbook.models import Pass, Barcode, StoreCard

CARDS_PATH = "wallet_cards"
SAVE_PATH_FOR_CARDS = Path(__file__).parent.parent / CARDS_PATH
load_dotenv()


def generate_apple_wallet_card(
    username: str
) -> None:
    name = username
    user = get_user_by_username(username)
    
    if user:
        logger.info(f'Got name {user.name} for user {username}')

        name = user.name

        logger.info(f'Setting name to {name}')

    cardInfo = StoreCard()
    cardInfo.addPrimaryField('Name', name, '')

    organizationName = 'MOSCOW CARD TM' 
    passTypeIdentifier = os.getenv("APPLE_TYPE_IDENTIFIER", None) 
    teamIdentifier = os.getenv("APPLE_TEAM_IDENTIFIER", None)

    passfile = Pass(cardInfo, \
        passTypeIdentifier=passTypeIdentifier, \
        organizationName=organizationName, \
        teamIdentifier=teamIdentifier)
    passfile.serialNumber = '1234567' 
    passfile.barcode = Barcode(message = 'Barcode message')    
    passfile.backgroundColor = '#BB0000'
    passfile.foregroundColor = '#FFFFFF'
    
    # Including the icon and logo is necessary for the passbook to be valid.
    passfile.addFile('icon.png', open('./cards/images/icon.png', 'rb'))
    passfile.addFile('logo.png', open('./cards/images/logo.png', 'rb'))
    
    save_path = SAVE_PATH_FOR_CARDS / f'{username}.pkpass'

    passfile.create('./cards/keys_certs/pass.pem', 
                    './cards/keys_certs/private.key', 
                    './cards/keys_certs/AppleWWDRCA.pem', 
                    None, save_path)

