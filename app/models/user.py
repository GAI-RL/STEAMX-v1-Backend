from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"
    MODERATOR = "moderator"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    
    # Contact & Profile
    phone_number = Column(String, nullable=True)
    school_name = Column(String, nullable=True)
    province = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    first_login_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    
    # Status & Roles
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.STUDENT)
    subscription_tier = Column(String, default="free")
    
    # Google OAuth fields
    google_id = Column(String, unique=True, nullable=True, index=True)
    profile_picture = Column(String, nullable=True)
    auth_provider = Column(String, default="local")
    
    # Relationships
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    
    # Feedback relationships - explicit foreign_keys to avoid ambiguity
    feedbacks = relationship("Feedback", foreign_keys="[Feedback.user_id]", back_populates="user", cascade="all, delete-orphan")
    assigned_feedbacks = relationship("Feedback", foreign_keys="[Feedback.assigned_to]", back_populates="assignee")
    
    uploaded_files = relationship("UploadedFile", back_populates="user", cascade="all, delete-orphan")
    usage_daily = relationship("UsageDaily", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("UserSubscription", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")