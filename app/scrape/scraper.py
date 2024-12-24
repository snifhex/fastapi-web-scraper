import re
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup as bs

from app.core.config import get_settings

settings = get_settings()

class WebScraper:
    def __init__(self):
        self.url = settings.URL_TO_SCRAPE

    def _get_product_title(self, product: bs):
        title = product.select_one("h2.woo-loop-product__title a")
        return title.get_text(strip=True)
    
    def _get_product_price(self, product: bs):
        price = product.select_one(".mf-product-price-box .price")
        if not price:
            return 0.0
        price_text = price.get_text(strip=True)
        match = re.search(r"(\d+(?:\.\d+)?)", price_text)
        if match:
            return float(match.group(1))
        return 0.0

    def _extract_product_image_url(self, product: bs):
        image = product.select_one(".mf-product-thumbnail img")
        if not image:
            return ""
        return image.get("data-lazy-src") or image.get("src") or ""
    
    def _save_image_to_s3(self, product: bs):
        image = self._extract_product_image_url(product)
        if not image:
            return None

    def _scrape_page(self, page: int, proxy: dict):
        if proxy:
            resp = requests.get(f'{self.url}page/{page}', proxies=proxy)
        else:
            resp = requests.get(f'{self.url}page/{page}')
        resp.raise_for_status()
        soup = bs(resp.content, "html.parser")

        products = soup.select("li.product")
        for product in products:
            product_title = self._get_product_title(product)
            product_price = self._get_product_price(product)
            path_to_image = self._save_image_to_s3(product)
            product_info = {
                "product_title": product_title,
                "product_price": product_price,
                "path_to_image": path_to_image
            }


    def scrape(self, pages: Optional[int] = 1, proxy: Optional[Dict] = None):
        for i in range(1, pages + 1):
            self._scrape_page(page=i, proxy=proxy)
        