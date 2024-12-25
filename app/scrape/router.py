from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from starlette import status

from app.common.cache.strategy import RedisCache
from app.common.notification.strategy import ConsoleNotification
from app.common.storage.strategy import S3ImageStorage
from app.core.auth import verify_api_key
from app.core.db import db_dependency
from app.scrape.schemas import JobResponse, ScraperStartSettingsRequest
from app.scrape.service import ScraperService
from app.utils.rate_limiter import limiter

scraper_router = APIRouter()


@scraper_router.post("/", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("5/second")
async def scrape_products(
    request: Request,
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
