from sqlalchemy import Column, String, Float, JSON, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base
from app.models.base import TimestampMixin

class Plan(Base, TimestampMixin):
    __tablename__ = "plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    title = Column(String(255), nullable=False)
    theme = Column(String(255), nullable=False)
    plan_type = Column(String(20), default='day_trip')
    status = Column(String(20), default='draft')
    mood_input = Column(JSON, nullable=False)
    conditions = Column(JSON, nullable=False)
    selected_area_id = Column(String(50), ForeignKey("areas.id"))
    itinerary = Column(JSON, nullable=False)
    estimated_budget = Column(JSON, nullable=False, default={})
    transportation = Column(JSON, nullable=False, default={})
    weather_info = Column(JSON, default={})
    mood_match_score = Column(Float)
    diversity_score = Column(Float)
    feasibility_score = Column(Float)
    mood_match_reason = Column(String)
    novelty_reason = Column(String)
    llm_generation_metadata = Column(JSON, default={})
    share_token = Column(String(100), unique=True)
    view_count = Column(Integer, default=0)
    save_count = Column(Integer, default=0)
    completion_count = Column(Integer, default=0)
