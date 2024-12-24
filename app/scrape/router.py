from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status

from app.common.cache.strategy import RedisCache
from app.common.notification.strategy import ConsoleNotification
from app.common.storage.strategy import S3ImageStorage
from app.core.config import get_settings
from app.core.db import db_dependency
from app.scrape.schemas import JobResponse, ScraperStartSettingsRequest
from app.scrape.service import ScraperService

scraper_router = APIRouter()

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")


async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key != get_settings().API_TOKEN:
        raise HTTPException(status_code=403, detail="Could not validate API key")
    return api_key


@scraper_router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def scrape_products(
    scraper_settings: ScraperStartSettingsRequest,
    background_tasks: BackgroundTasks,
    db: db_dependency,
    _: str = Depends(verify_api_key),
) -> JobResponse:
    try:
        service = ScraperService(
            db=db, image_storage=S3ImageStorage(), cache=RedisCache(), notifier=ConsoleNotification()
        )

        background_tasks.add_task(service.start_scraping, scraper_settings)

        return JobResponse(message="Scraping job started")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
