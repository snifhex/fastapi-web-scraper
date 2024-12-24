import json
from typing import Any, Optional

import redis

from app.common.cache.abstract import CacheStrategy
from app.core.config import get_settings


class RedisCache(CacheStrategy):
    def __init__(self):
        self.redis = redis.Redis(
            host=get_settings().REDIS_HOST,
            port=get_settings().REDIS_PORT,
            db=get_settings().REDIS_DB,
            decode_responses=True,
        )

    def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            self.redis.set(key, value, ex=expire)
            return True
        except (redis.RedisError, TypeError, ValueError):
            return False

    def exists(self, key: str) -> bool:
        return bool(self.redis.exists(key))

    def get_product_cache_key(self, product_title: str) -> str:
        return f"product:{product_title}"
