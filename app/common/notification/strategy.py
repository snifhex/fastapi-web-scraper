import logging
from typing import Any, Dict, Optional

from app.common.notification.abstract import NotificationStrategy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConsoleNotification(NotificationStrategy):
    def notify(self, message: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        try:
            if metadata:
                logger.info("%s | Metadata: %s", message, metadata)
            else:
                logger.info(message)
            return True
        except Exception:
            return False
