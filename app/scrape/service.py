import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.common.cache.abstract import CacheStrategy
from app.common.cache.strategy import RedisCache
from app.common.notification.abstract import NotificationStrategy
from app.common.notification.strategy import ConsoleNotification
from app.common.storage.abstract import ImageStorage
from app.common.storage.strategy import S3ImageStorage
from app.scrape.models import Product
from app.scrape.schemas import ProductCreate, ScraperStartSettingsRequest
from app.scrape.scraper import WebScraper

logger = logging.getLogger(__name__)


class ScraperService:
    def __init__(
        self,
        db: Session,
        image_storage: ImageStorage | S3ImageStorage,
        cache: Optional[CacheStrategy | RedisCache] = None,
        notifier: Optional[NotificationStrategy | ConsoleNotification] = None,
    ):
        self.db = db
        self.image_storage = image_storage
        self.cache = cache
        self.notifier = notifier
        self.stats = {"total_products": 0, "updated_products": 0, "new_products": 0}

    def _process_product(self, product: ProductCreate) -> None:
        try:
            self.stats["total_products"] += 1

            s3_image_url = self.image_storage.upload_image(product.path_to_image)
            if not s3_image_url:
                logger.error("Failed to upload image for product: %s", product.product_title)
                return

            product.path_to_image = s3_image_url

            cache_key = None
            if self.cache:
                cache_key = self.cache.get_product_cache_key(product.product_title)

            existing = self.db.query(Product).filter(Product.product_title == product.product_title).first()

            if existing:
                if existing.product_price != product.product_price:
                    existing.product_price = product.product_price
                    existing.path_to_image = product.path_to_image
                    self.db.commit()
                    self.stats["updated_products"] += 1
                    if self.cache:
                        self.cache.set(cache_key, product.product_price)
            else:
                db_product = Product(**product.model_dump())
                self.db.add(db_product)
                self.db.commit()
                self.stats["new_products"] += 1
                if self.cache:
                    self.cache.set(cache_key, product.product_price)

            if self.notifier and self.stats["total_products"] % 10 == 0:
                self.notifier.notify(
                    f"Progress update - Processed: {self.stats['total_products']}, "
                    f"Updated: {self.stats['updated_products']}, "
                    f"New: {self.stats['new_products']}"
                )

        except Exception as e:
            logger.error("Error processing product: %s", e)

    def start_scraping(self, settings: Optional[ScraperStartSettingsRequest] = None) -> None:
        try:
            self.stats = {"total_products": 0, "updated_products": 0, "new_products": 0}

            scraper = WebScraper()
            for product in scraper.scrape(settings):
                self._process_product(product)

            if self.notifier:
                message = (
                    f"Scraping completed. "
                    f"Total: {self.stats['total_products']}, "
                    f"Updated: {self.stats['updated_products']}, "
                    f"New: {self.stats['new_products']}"
                )
                self.notifier.notify(message, self.stats)

        except Exception as e:
            error_message = f"Scraping job failed: {e!s}"
            logger.error(error_message)
            if self.notifier:
                self.notifier.notify(error_message)
