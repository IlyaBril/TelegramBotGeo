import os

from dotenv import load_dotenv
from pydantic import SecretStr, StrictStr, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class SiteSettings(BaseSettings):
    #Telegramm Api Key:
    tg_api: SecretStr = os.getenv("TG_API", None)
    #Geoapigy GeoPlaces Api Key:
    geo_api_key: StrictStr = os.getenv("GEO_SITE_API", None)

site = SiteSettings()