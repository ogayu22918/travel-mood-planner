from sqlalchemy import Column, String, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geography
import uuid

from app.core.database import Base
from app.models.base import TimestampMixin

class Area(Base, TimestampMixin):
    __tablename__ = "areas"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    name_en = Column(String(100))
    prefecture = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    boundary = Column(Geography(geometry_type='POLYGON', srid=4326))
    center_point = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    characteristics = Column(JSON, default={})
    transport_hub = Column(JSON, default={})
    seasonal_info = Column(JSON, default={})
    popularity_rank = Column(Float)
