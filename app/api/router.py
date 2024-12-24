from fastapi import APIRouter

from app.scrape.router import scraper_router

api_router = APIRouter()

api_router.include_router(scraper_router, prefix="/scrape", tags=["scrape"])
