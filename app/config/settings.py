import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    SHOPIFY_API_KEY: str = os.getenv("SHOPIFY_API_KEY", "")
    SHOPIFY_PASSWORD: str = os.getenv("SHOPIFY_PASSWORD", "")
    SHOPIFY_STORE_URL: str = os.getenv("SHOPIFY_STORE_URL", "")

    MONITOR_STATUS_URL: str = os.getenv("MONITOR_STATUS_URL", "")

    DEFAULT_CHAT_ID: int = int(os.getenv("DEFAULT_CHAT_ID", 0))
    DEFAULT_CURRENCY: str = "USD"

    BRAND_NAME: str = "Samarkand Soul"
    BRAND_MISSION: str = "Calm Luxury & Human + AI Synergy"

    LLM_MODEL: str = "gpt-5.1"
    TEMPERATURE: float = 0.4

settings = Settings()
