from fastapi import APIRouter

scraper_router = APIRouter()

@scraper_router.post("/")
async def scrape():
    return {"message": "Scraping data"}