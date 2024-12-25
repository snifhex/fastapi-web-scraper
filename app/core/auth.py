from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.core.config import get_settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != get_settings().API_TOKEN:
        raise HTTPException(status_code=403, detail="Could not validate API key")
    return api_key
