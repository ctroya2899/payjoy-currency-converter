from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """ App Settings loaded from environment variables"""

    exchange_rate_api_key: str
    exchange_rate_base_url: str 
    http_timeout_seconds: float = 5.0
    cache_ttl_seconds: int = 300


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()