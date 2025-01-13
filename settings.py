import os

from dotenv import load_dotenv
from pydantic import SecretStr, StrictStr, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv("SITE_API", None)
    host_api: StrictStr = os.getenv("HOST_API", None)
    tg_api: SecretStr = os.getenv("TG_API", None)
    geo_api_key: StrictStr = os.getenv("GEO_SITE_API", None)
    geo_api_host: StrictStr = os.getenv("GEO_HOST", None)

