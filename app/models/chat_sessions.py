from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.database import Base

class SessionStatus(str, enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=True)
    grade_id = Column(UUID(as_uuid=True), ForeignKey("grades.id"), nullable=True)
    title = Column(String, default="New Conversation")
    total_qa_pairs = Column(Integer, default=0)
    total_tokens_used = Column(BigInteger, nullable=True)
    status = Column(SQLAlchemyEnum(SessionStatus), default=SessionStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    subject = relationship("Subject", back_populates="chat_sessions")
    grade = relationship("Grade", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    system_messages = relationship("SystemMessage", back_populates="session", cascade="all, delete-orphan")