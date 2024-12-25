from fastapi import APIRouter, FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.router import api_router
from app.core.db import Base, engine
from app.utils.rate_limiter import limiter

app = FastAPI(
    title="Scraper API",
    description="Simple webscraper built with fastapi, postgres and redis.",
    version="1.0.0",
    docs_url="/docs",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

Base.metadata.create_all(bind=engine)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(api_router)
app.include_router(api_v1_router)
