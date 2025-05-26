from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from app.api.v1.router import api_router
from app.core.database import engine, Base
from app.core.cache import redis_client
from app.config import settings
from app.utils.logger import setup_logging

setup_logging()
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Travel Mood API", version=settings.VERSION)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await redis_client.ping()
    
    yield
    
    await redis_client.close()
    await engine.dispose()
    logger.info("Shutting down Travel Mood API")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Travel Mood API is running!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": "travel-mood-api"
    }
