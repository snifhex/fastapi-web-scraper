import base64
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_TOKEN: str = "super"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/scraped"
    URL_TO_SCRAPE: str = base64.b64decode("aHR0cHM6Ly9kZW50YWxzdGFsbC5jb20vc2hvcC8=").decode("utf-8")
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    AWS_ACCESS_KEY_ID: str = "minioadmin"
    AWS_SECRET_ACCESS_KEY: str = "minioadmin"
    AWS_BUCKET_NAME: str = "scraper-bucket"
    AWS_ENDPOINT_URL: str = "http://localhost:9000"
    MAX_RETRIES: int = 3
    MAX_DELAY: int = 5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
