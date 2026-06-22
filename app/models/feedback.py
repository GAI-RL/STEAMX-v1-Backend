from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.database import Base

class FeedbackType(str, enum.Enum):
    CONTACT_FORM = "contact_form"
    QA_RATING = "qa_rating"
    GENERAL = "general"

class FeedbackStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    SPAM = "spam"

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey("chat_messages.id"), nullable=True)
    feedback_type = Column(SQLAlchemyEnum(FeedbackType), nullable=False)
    
    # Contact form fields
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    topic = Column(String, nullable=True)
    institution = Column(String, nullable=True)
    subject_line = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    
    # Rating for Q&A
    rating = Column(Integer, nullable=True)
    comment = Column(Text, nullable=True)
    
    # Admin fields
    status = Column(SQLAlchemyEnum(FeedbackStatus), default=FeedbackStatus.NEW)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - explicit foreign_keys
    user = relationship("User", foreign_keys=[user_id], back_populates="feedbacks")
    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_feedbacks")
    chat_message = relationship("ChatMessage", back_populates="feedbacks")