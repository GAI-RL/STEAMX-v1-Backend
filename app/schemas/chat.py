from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

# Request schemas
class SendMessageRequest(BaseModel):
    session_id: UUID
    question: str

# Figure response schema
class FigureResponse(BaseModel):
    image_path: str
    caption: str
    score: float
    image_base64: Optional[str] = None
    media_type: str = "image/png"

# Response schemas
class ChatMessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChatSessionWithMessages(BaseModel):
    session: ChatSessionResponse
    messages: list[ChatMessageResponse]

class SendMessageResponse(BaseModel):
    question: str
    answer: str
    session_id: UUID
    figures: list[FigureResponse] = []