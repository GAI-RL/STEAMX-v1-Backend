from sqlalchemy import Column, Integer, BigInteger, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class UsageDaily(Base):
    __tablename__ = "usage_daily"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    sessions_created = Column(Integer, default=0)
    qa_pairs_completed = Column(Integer, default=0)
    tokens_used = Column(BigInteger, nullable=True)
    files_uploaded = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="usage_daily")