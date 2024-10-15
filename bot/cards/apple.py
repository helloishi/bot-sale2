import os
from pathlib import Path

from dotenv import load_dotenv

from passbook.passbook.models import Pass, Barcode, StoreCard

SAVE_PATH_FOR_CARDS = Path(__file__).parent.parent.parent / "wallet_cards"
load_dotenv()


def generate_apple_wallet_card(
    name: str
) -> None:
    cardInfo = StoreCard()
    #cardInfo.addPrimaryField('name', name, 'Name')

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
    # Including the icon and logo is necessary for the passbook to be valid.
    passfile.addFile('icon.png', open('./images/icon.png', 'rb'))
    passfile.addFile('logo.png', open('./images/logo.png', 'rb'))
    
    save_path = SAVE_PATH_FOR_CARDS / f'{name}.pkpass'

    passfile.create('keys_certs/pass.pem', 
                    'keys_certs/private.key', 
                    'keys_certs/AppleWWDRCA.pem', 
                    None, save_path)


generate_apple_wallet_card("daniildiveev")
