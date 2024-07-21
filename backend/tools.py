import re

TELEGRAM_LINK_REGEX = r't\.me\/(\w+)'

def validate_username(username: str) -> str:
    username = username.replace("@", "")
    match = re.match(r't\.me\/(\w+)', username)
    
    if match:
        username = match.group(1)

    return username.lower()