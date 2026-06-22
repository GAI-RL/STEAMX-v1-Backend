from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime
from app.models.chat_sessions import ChatSession, SessionStatus
from app.models.chat_messages import ChatMessage
from app.models.user import User
from app.models.subject import Subject
from app.models.grade import Grade
from app.models.usage_daily import UsageDaily
from app.models.uploaded_file import UploadedFile
from app.models.message_attachment import MessageAttachment
from app.services.rag_service import RAGService

class ChatService:
    
    @staticmethod
    def create_session(db: Session, user: User, subject_id: UUID, grade_id: UUID) -> ChatSession:
        """Create a new chat session with subject and grade"""
        
        # Verify subject exists
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid subject_id"
            )
        
        # Verify grade exists
        grade = db.query(Grade).filter(Grade.id == grade_id).first()
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid grade_id"
            )
        
        session = ChatSession(
            user_id=user.id,
            subject_id=subject_id,
            grade_id=grade_id,
            title="New Conversation",
            status=SessionStatus.ACTIVE,
            total_qa_pairs=0
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_user_sessions(db: Session, user: User) -> list[ChatSession]:
        """Get all chat sessions for a user"""
        
        sessions = db.query(ChatSession)\
            .filter(ChatSession.user_id == user.id, ChatSession.status == SessionStatus.ACTIVE)\
            .order_by(ChatSession.updated_at.desc())\
            .all()
        return sessions
    
    @staticmethod
    def get_session_with_messages(db: Session, session_id: UUID, user: User):
        """Get a specific session with all Q&A pairs"""
        
        session = db.query(ChatSession)\
            .filter(ChatSession.id == session_id, ChatSession.user_id == user.id)\
            .first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Get all Q&A messages (one row per Q&A pair)
        messages = db.query(ChatMessage)\
            .filter(ChatMessage.session_id == session_id)\
            .order_by(ChatMessage.created_at.asc())\
            .all()
        
        return {"session": session, "messages": messages}
    
    @staticmethod
    async def send_message(db: Session, session_id: UUID, prompt: str, user: User, file_ids: list[UUID] = None) -> dict:
        """Send a prompt and get AI response (stores as one Q&A row)"""
        
        # Verify session belongs to user
        session = db.query(ChatSession)\
            .filter(ChatSession.id == session_id, ChatSession.user_id == user.id)\
            .first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Get subject and grade info for context
        subject = db.query(Subject).filter(Subject.id == session.subject_id).first()
        grade = db.query(Grade).filter(Grade.id == session.grade_id).first()
        
        # Build system context
        system_context = f"You are a tutor helping a {grade.level}th grade student with {subject.name}. Provide clear, educational responses."
        
        # Get previous Q&A pairs for context
        previous_qa = db.query(ChatMessage)\
            .filter(ChatMessage.session_id == session_id)\
            .order_by(ChatMessage.created_at.asc())\
            .all()
        
        # Format history for AI
        chat_history = []
        for qa in previous_qa:
            chat_history.append({"role": "user", "content": qa.prompt})
            chat_history.append({"role": "assistant", "content": qa.response})
        
        # Call RAG service with selected grade + subject from this chat session
        rag_service = RAGService()
        rag_result = await rag_service.get_answer(
            question=prompt,
            chat_history=chat_history,
            system_context=system_context,
            session_id=str(session.id),
            subject_id=str(subject.id),
            subject_name=subject.name,
            grade_id=str(grade.id),
            grade_level=grade.level,
        )
        response = rag_result.get("answer", "")
        figures = rag_result.get("figures", [])
        
        # Save Q&A as one row
        new_qa = ChatMessage(
            session_id=session_id,
            prompt=prompt,
            response=response,
            response_version=1,
            previous_responses=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_qa)
        db.flush() # Flush to get the new_qa.id for attachments
        
        # Link files to the message
        files_count = 0
        if file_ids:
            for file_id in file_ids:
                # Verify file exists and belongs to user
                uploaded_file = db.query(UploadedFile).filter(
                    UploadedFile.id == file_id,
                    UploadedFile.user_id == user.id
                ).first()
                
                if uploaded_file:
                    attachment = MessageAttachment(
                        message_id=new_qa.id,
                        file_id=file_id
                    )
                    db.add(attachment)
                    uploaded_file.is_processed = True
                    files_count += 1
        
        # Update session
        session.total_qa_pairs += 1
        session.updated_at = datetime.utcnow()
        
        # Update session title with first prompt (if not set)
        if session.title == "New Conversation" and prompt:
            session.title = prompt[:50] + ("..." if len(prompt) > 50 else "")
        
        # Update usage_daily
        today = datetime.utcnow().date()
        usage = db.query(UsageDaily).filter(
            UsageDaily.user_id == user.id,
            UsageDaily.date == today
        ).first()
        
        if usage:
            usage.qa_pairs_completed += 1
            usage.files_uploaded += files_count
            usage.updated_at = datetime.utcnow()
        else:
            usage = UsageDaily(
                user_id=user.id,
                date=today,
                sessions_created=1,
                qa_pairs_completed=1,
                files_uploaded=files_count
            )
            db.add(usage)
        
        db.commit()
        db.refresh(new_qa)
        
        return {
            "message_id": new_qa.id,
            "session_id": session_id,
            "prompt": prompt,
            "response": response,
            "response_version": 1,
            "created_at": new_qa.created_at,
            "figures": figures,
            "attachments": new_qa.attachments
        }
    
    @staticmethod
    async def regenerate_response(db: Session, message_id: UUID, user: User) -> dict:
        """Regenerate a response for an existing prompt"""
        
        # Get the Q&A pair
        qa = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
        if not qa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Verify session belongs to user
        session = db.query(ChatSession).filter(
            ChatSession.id == qa.session_id,
            ChatSession.user_id == user.id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Get subject and grade for context
        subject = db.query(Subject).filter(Subject.id == session.subject_id).first()
        grade = db.query(Grade).filter(Grade.id == session.grade_id).first()
        
        # Build system context
        system_context = f"You are a tutor helping a {grade.level}th grade student with {subject.name}. Provide clear, educational responses."
        
        # Save current response to previous_responses
        previous_responses = qa.previous_responses or []
        previous_responses.append({
            "version": qa.response_version,
            "response": qa.response,
            "created_at": datetime.utcnow().isoformat()
        })
        
        # Call RAG service for new response with the same selected grade + subject
        rag_service = RAGService()
        rag_result = await rag_service.get_answer(
            question=qa.prompt,
            chat_history=[],
            system_context=system_context,
            session_id=str(session.id),
            subject_id=str(subject.id),
            subject_name=subject.name,
            grade_id=str(grade.id),
            grade_level=grade.level,
        )
        new_response = rag_result.get("answer", "")
        figures = rag_result.get("figures", [])
        
        # Update the Q&A pair
        qa.previous_responses = previous_responses
        qa.response_version += 1
        qa.response = new_response
        qa.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "message_id": qa.id,
            "response": new_response,
            "response_version": qa.response_version,
            "figures": figures,
        }
    
    @staticmethod
    def delete_session(db: Session, session_id: UUID, user: User):
        """Soft delete a chat session (mark as deleted)"""
        
        session = db.query(ChatSession)\
            .filter(ChatSession.id == session_id, ChatSession.user_id == user.id)\
            .first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Soft delete - mark as deleted
        session.status = SessionStatus.DELETED
        session.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Session deleted successfully"}