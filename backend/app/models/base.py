from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from app.core.database import Base

class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
