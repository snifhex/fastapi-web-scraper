import logging
import time
from functools import wraps
from typing import Callable, TypeVar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


T = TypeVar("T")


def retry(retries: int = 3, delay: int = 1):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    logger.error("Failed to scrape the page, Retrying...")
                    if attempt == retries - 1:
                        logger.error("Max retries reached, aborting...")
                        raise
                    time.sleep(delay)
            return None

        return wrapper

    return decorator
