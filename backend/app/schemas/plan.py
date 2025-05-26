from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID

class ItineraryItem(BaseModel):
    time_slot: str
    spot_id: str
    spot_name: str
    activity: str
    duration_min: int
    tips: Optional[str] = None

class Plan(BaseModel):
    id: str
    title: str
    theme: str
    itinerary: List[ItineraryItem]
    estimated_budget: Dict[str, Any]
    transportation: Dict[str, Any]
    mood_match_score: float
    mood_match_reason: str
    novelty_points: List[str]

class PlanGenerationRequest(BaseModel):
    area_id: str
    mood: "MoodInput"
    conditions: "ConditionsInput"
    plan_count: int = 5

class PlanGenerationResponse(BaseModel):
    plans: List[Plan]
    metadata: Dict[str, Any]

from app.schemas.common import MoodInput, ConditionsInput
PlanGenerationRequest.model_rebuild()
