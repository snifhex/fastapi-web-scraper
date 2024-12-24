from abc import ABC, abstractmethod
from typing import Optional


class ImageStorage(ABC):
    @abstractmethod
    def upload_image(self, image_url: str) -> Optional[str]:
        pass
