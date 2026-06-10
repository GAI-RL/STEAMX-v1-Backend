from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Request Schemas
class CreateSessionRequest(BaseModel):
    subject_id: UUID
    grade_id: UUID

class SendMessageRequest(BaseModel):
    session_id: UUID
    prompt: str  # Changed from 'question' to 'prompt'

class RegenerateResponseRequest(BaseModel):
    message_id: UUID

# Response Schemas
class ChatMessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    prompt: str
    response: str
    response_version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    id: UUID
    title: str
    subject_id: Optional[UUID] = None
    grade_id: Optional[UUID] = None
    total_qa_pairs: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatSessionWithMessages(BaseModel):
    id: UUID
    title: str
    subject_id: Optional[UUID] = None
    grade_id: Optional[UUID] = None
    total_qa_pairs: int
    status: str
    created_at: datetime
    updated_at: datetime
    messages: list[ChatMessageResponse]

    class Config:
        from_attributes = True

class SendMessageResponse(BaseModel):
    message_id: UUID
    session_id: UUID
    prompt: str
    response: str
    response_version: int
    created_at: datetime

class RegenerateResponseResponse(BaseModel):
    message_id: UUID
    response: str
    response_version: int