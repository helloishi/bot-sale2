from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class BotSettings(BaseSettings):
    bot_token: SecretStr
    redirect_link: str
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = BotSettings()