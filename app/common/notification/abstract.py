from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class NotificationStrategy(ABC):
    @abstractmethod
    def notify(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        pass
