from sqlalchemy import Column, Text, Integer, BigInteger, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False)
    
    # One row per Q&A pair
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    
    # Versioning for regenerated responses
    response_version = Column(Integer, default=1)
    previous_responses = Column(JSON, nullable=True)
    
    # Token tracking (nullable for now)
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    
    # Changed from 'metadata' to 'message_metadata' (SQLAlchemy reserved word)
    message_metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")
    attachments = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="message")