from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid

from app.core.database import Base
from app.models.base import TimestampMixin

class VectorData(Base, TimestampMixin):
    __tablename__ = "vectors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    vector_type = Column(String(50), default='description')
    embedding = Column(Vector(1536), nullable=False)
    text_source = Column(Text)
    model_version = Column(String(50), default='text-embedding-ada-002')
