from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    price_monthly_pkr = Column(Integer, nullable=False)
    qa_pairs_per_day = Column(Integer, nullable=False)
    sessions_per_day = Column(Integer, nullable=False)
    max_file_uploads = Column(Integer, nullable=False)
    max_file_size_bytes = Column(BigInteger, nullable=False)
    rag_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user_subscriptions = relationship("UserSubscription", back_populates="plan")