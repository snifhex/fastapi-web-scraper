from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import get_settings

limiter = Limiter(
    key_func=get_remote_address, storage_uri=f"redis://{get_settings().REDIS_HOST}:{get_settings().REDIS_PORT}/n"
)
