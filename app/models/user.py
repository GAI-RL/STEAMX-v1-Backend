from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)  # ← Changed to nullable (for Google users)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
    subscription_tier = Column(String, default="free")
    
    # Google OAuth fields
    google_id = Column(String, unique=True, nullable=True, index=True)  # ← NEW
    profile_picture = Column(String, nullable=True)  # ← NEW
    auth_provider = Column(String, default="local")  # 'local' or 'google'  # ← NEW
    
    # Relationships
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")