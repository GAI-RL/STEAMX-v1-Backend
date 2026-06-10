from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.subject import Subject
from app.models.grade import Grade
from app.schemas.chat import (
    CreateSessionRequest,
    SendMessageRequest,
    RegenerateResponseRequest,
    ChatSessionResponse,
    ChatSessionWithMessages,
    SendMessageResponse,
    RegenerateResponseResponse,
    ChatMessageResponse
)
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_session(
    request: CreateSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new chat session with subject and grade"""
    
    # Verify subject exists
    subject = db.query(Subject).filter(Subject.id == request.subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subject_id"
        )
    
    # Verify grade exists
    grade = db.query(Grade).filter(Grade.id == request.grade_id).first()
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid grade_id"
        )
    
    return ChatService.create_session(db, current_user, request.subject_id, request.grade_id)

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
    """Get a specific session with all Q&A pairs"""
    return ChatService.get_session_with_messages(db, session_id, current_user)

@router.post("/message", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a prompt and get AI response (stores as one Q&A row)"""
    return await ChatService.send_message(
        db, 
        request.session_id, 
        request.prompt, 
        current_user
    )

@router.post("/message/regenerate", response_model=RegenerateResponseResponse)
async def regenerate_response(
    request: RegenerateResponseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Regenerate a response for an existing prompt"""
    return await ChatService.regenerate_response(
        db,
        request.message_id,
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