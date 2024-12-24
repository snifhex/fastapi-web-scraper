import logging
import re
from typing import Dict, Iterator, Optional

import requests
from bs4 import BeautifulSoup as bs

from app.core.config import get_settings
from app.scrape.schemas import ProductCreate, ScraperStartSettingsRequest
from app.utils.retry import retry

settings = get_settings()


class WebScraper:
    def __init__(self):
        self.BASE_URL = settings.URL_TO_SCRAPE

    def _get_product_title(self, product: bs) -> str:
        title = product.select_one("h2.woo-loop-product__title a")
        return title.get_text(strip=True)

    def _get_product_price(self, product: bs) -> float:
        price = product.select_one(".mf-product-price-box .price")
        if not price:
            return 0.0
        price_text = price.get_text(strip=True)
        match = re.search(r"(\d+(?:\.\d+)?)", price_text)
        if match:
            return float(match.group(1))
        return 0.0

    def _extract_product_image_url(self, product: bs) -> str:
        image = product.select_one(".mf-product-thumbnail img")
        if not image:
            return ""
        return image.get("data-lazy-src") or image.get("src") or ""

    @retry(retries=get_settings().MAX_RETRIES, delay=get_settings().MAX_DELAY)
    def _fetch_page(self, url: str, proxy: Optional[Dict] = None) -> bs:
        resp = requests.get(url, proxies=proxy if proxy else None)
        resp.raise_for_status()
        return bs(resp.content, "html.parser")

    def _scrape_page(self, page: int, proxy: Optional[Dict] = None) -> Iterator[ProductCreate]:
        try:
            url = f"{self.BASE_URL}page/{page}" if page > 1 else self.BASE_URL
            soup = self._fetch_page(url, proxy=proxy)
            products = soup.select("li.product")
            for product in products:
                product_title = self._get_product_title(product)
                product_price = self._get_product_price(product)
                path_to_image = self._extract_product_image_url(product)
                yield ProductCreate(
                    product_title=product_title,
                    product_price=product_price,
                    path_to_image=path_to_image,
                )

        except Exception as e:
            logging.error("Error scraping page %d: %s", page, str(e))

    def scrape(self, settings: Optional[ScraperStartSettingsRequest] = None) -> Iterator[ProductCreate]:
        page_limit = settings.page_limit if settings else 1
        proxy = {"http": settings.proxy, "https": settings.proxy} if settings and settings.proxy else None

        for page in range(1, page_limit + 1):
            yield from self._scrape_page(page=page, proxy=proxy)
