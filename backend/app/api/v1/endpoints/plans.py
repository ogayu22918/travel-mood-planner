from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import structlog
import uuid

from app.api.deps import get_current_user_optional
from app.core.database import get_db
from app.schemas.plan import (
    PlanGenerationRequest,
    PlanGenerationResponse,
    Plan
)

router = APIRouter()
logger = structlog.get_logger()

@router.post("/generate", response_model=PlanGenerationResponse)
async def generate_plans(
    request: PlanGenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_optional)
):
    try:
        # ダミーのプラン生成
        plans = []
        for i in range(3):
            plan = Plan(
                id=str(uuid.uuid4()),
                title=f"プラン{i+1}: {request.area_id}の魅力を満喫",
                theme="定番スポット巡り" if i == 0 else "隠れた名所探訪",
                itinerary=[
                    {
                        "time_slot": "午前",
                        "spot_id": str(uuid.uuid4()),
                        "spot_name": f"スポット{j+1}",
                        "activity": "観光と写真撮影",
                        "duration_min": 90,
                        "tips": "混雑を避けるなら早朝がおすすめ"
                    }
                    for j in range(3)
                ],
                estimated_budget={
                    "total": 5000,
                    "breakdown": "交通費1000円、食事3000円、入場料1000円"
                },
                transportation={
                    "primary": "電車",
                    "details": "JR線と地下鉄を利用"
                },
                mood_match_score=0.85,
                mood_match_reason="リラックスしたい気分にぴったりの穏やかなプランです",
                novelty_points=["新しい発見1", "新しい発見2"]
            )
            plans.append(plan)
        
        return PlanGenerationResponse(
            plans=plans,
            metadata={
                "generation_time_ms": 1500,
                "spot_count": 9,
                "confidence_scores": [0.85, 0.82, 0.80]
            }
        )
        
    except Exception as e:
        logger.error("Plan generation failed", error=str(e))
        raise HTTPException(status_code=500, detail="プラン生成に失敗しました")
