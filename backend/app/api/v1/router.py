from fastapi import APIRouter

from app.api.v1.endpoints import areas, plans, health

api_router = APIRouter()

api_router.include_router(areas.router, prefix="/areas", tags=["areas"])
api_router.include_router(plans.router, prefix="/plans", tags=["plans"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
