from fastapi import APIRouter

from app.scrape.scraper import WebScraper

scraper_router = APIRouter()


@scraper_router.post("/")
async def scrape():
    scraper = WebScraper()
    scraper.scrape()
    return {"message": "Scraping data"}
