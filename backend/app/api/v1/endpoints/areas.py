from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import structlog
from datetime import datetime

from app.api.deps import get_current_user_optional
from app.core.database import get_db
from app.schemas.area import (
    AreaRecommendationRequest,
    AreaRecommendationResponse
)
from app.services.area_service import AreaService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService

router = APIRouter()
logger = structlog.get_logger()

@router.post("/recommend", response_model=AreaRecommendationResponse)
async def recommend_areas(
    request: AreaRecommendationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    try:
        embedding_service = EmbeddingService()
        llm_service = LLMService()
        area_service = AreaService(db, embedding_service, llm_service)
        
        recommendations = await area_service.recommend_areas(
            mood_input=request.mood,
            conditions=request.conditions,
            user_location=request.location
        )
        
        return AreaRecommendationResponse(
            recommendations=recommendations,
            generated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("Area recommendation failed", error=str(e))
        raise HTTPException(status_code=500, detail="エリア推薦の生成に失敗しました")
