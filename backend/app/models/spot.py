from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
import uuid

from app.core.database import Base
from app.models.base import TimestampMixin

class Spot(Base, TimestampMixin):
    __tablename__ = "spots"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    google_place_id = Column(String(255), unique=True)
    name = Column(String(255), nullable=False)
    name_en = Column(String(255))
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    area_id = Column(String(50), ForeignKey("areas.id"))
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100))
    price_range = Column(Integer)
    price_info = Column(JSON, default={})
    metadata = Column(JSON, default={})
    contact_info = Column(JSON, default={})
    business_hours = Column(JSON, default={})
    popularity_score = Column(Float, default=0.5)
    uniqueness_score = Column(Float, default=0.5)
    family_friendly_score = Column(Float)
    accessibility_score = Column(Float)
    avg_duration_min = Column(Integer, default=60)
    min_duration_min = Column(Integer, default=30)
    max_duration_min = Column(Integer, default=180)
    weather_dependency = Column(String(20))
    is_active = Column(Boolean, default=True)
    
    area = relationship("Area", backref="spots")
