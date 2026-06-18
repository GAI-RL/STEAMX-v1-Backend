from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Any

# Request Schemas
class CreateSessionRequest(BaseModel):
    subject_id: UUID
    grade_id: UUID

class SendMessageRequest(BaseModel):
    session_id: UUID
    prompt: str

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
    figures: list[Any] = []

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
    # This matches ChatService.get_session_with_messages(), which returns:
    # {"session": session, "messages": messages}
    session: ChatSessionResponse
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
    figures: list[Any] = []

class RegenerateResponseResponse(BaseModel):
    message_id: UUID
    response: str
    response_version: int
    figures: list[Any] = []
