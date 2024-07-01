from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class BotSettings(BaseSettings):
    bot_token: SecretStr
    login_link: str
    web_app_link: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

class DBSettings(BaseSettings):
    db_host: str
    db_name: str
    db_port: int
    db_user: str
    db_pass: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = BotSettings()
db_config = DBSettings()