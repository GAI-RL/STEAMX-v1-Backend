from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.chat import (
    SendMessageRequest,
    ChatSessionResponse,
    ChatSessionWithMessages,
    SendMessageResponse
)
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new chat session"""
    return ChatService.create_session(db, current_user)

@router.get("/sessions", response_model=list[ChatSessionResponse])
async def get_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all user's chat sessions"""
    return ChatService.get_user_sessions(db, current_user)

@router.get("/sessions/{session_id}", response_model=ChatSessionWithMessages)
async def get_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific session with all messages"""
    return ChatService.get_session_with_messages(db, session_id, current_user)

@router.post("/message", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a message and get RAG response"""
    return await ChatService.send_message(
        db, 
        request.session_id, 
        request.question, 
        current_user
    )

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a chat session"""
    return ChatService.delete_session(db, session_id, current_user)