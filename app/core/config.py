import base64
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/scraped"
    URL_TO_SCRAPE: str = base64.b64decode("aHR0cHM6Ly9kZW50YWxzdGFsbC5jb20vc2hvcC8=").decode("utf-8")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
