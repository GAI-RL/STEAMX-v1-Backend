

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class Grade(Base):
    __tablename__ = "grades"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    level = Column(Integer, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    
    # Relationships
    chat_sessions = relationship("ChatSession", back_populates="grade")