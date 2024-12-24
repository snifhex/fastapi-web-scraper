from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    product_title: str = Field(..., description="Title of the product")
    product_price: float = Field(..., description="Price of the product")
    path_to_image: str = Field(..., description="Path to the product image")


class ProductCreate(ProductBase):
    pass

class ScraperStartSettingsRequest(BaseModel):
    page_limit: Optional[int] = Field(None, description="Limit the number of pages to scrape")
    proxy: Optional[str] = Field(None, description="Proxy string to use for scraping")

class JobResponse(BaseModel):
    message: str = "Scraping job started"
