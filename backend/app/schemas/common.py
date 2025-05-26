from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class LocationInput(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class MoodInput(BaseModel):
    text: Optional[str] = Field(None, max_length=500)
    presets: List[str] = Field(default_factory=list)
    exploration_score: float = Field(0.5, ge=0, le=1)

class ConditionsInput(BaseModel):
    party_size: int = Field(1, ge=1, le=20)
    budget: str = Field("medium", pattern="^(low|medium|high)$")
    duration: int = Field(8, ge=1, le=24)
    date: Optional[datetime] = None

class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
