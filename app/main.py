from fastapi import APIRouter, FastAPI

from app.api.router import api_router
from app.core.db import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(api_router)
app.include_router(api_v1_router)
