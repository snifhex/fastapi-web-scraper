from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheStrategy(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass
