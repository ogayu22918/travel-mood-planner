from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class AreaBase(BaseModel):
    id: str
    name: str
    name_en: Optional[str] = None
    prefecture: str
    region: str

class AreaRecommendation(AreaBase):
    match_score: float = Field(..., ge=0, le=1)
    primary_reason: str
    detailed_reason: str
    key_spots: List[str]
    expected_experience: str
    accessibility: Dict[str, Any]
    tips: str

class AreaRecommendationRequest(BaseModel):
    mood: "MoodInput"
    conditions: "ConditionsInput"
    location: "LocationInput"

class AreaRecommendationResponse(BaseModel):
    recommendations: List[AreaRecommendation]
    generated_at: datetime
    cache_ttl: int = 300

from app.schemas.common import MoodInput, ConditionsInput, LocationInput
AreaRecommendationRequest.model_rebuild()
