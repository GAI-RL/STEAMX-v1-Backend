from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.models.chat import ChatSession, ChatMessage
from app.models.user import User
from app.services.rag_service import RAGService

class ChatService:
    
    @staticmethod
    def create_session(db: Session, user: User) -> ChatSession:
        """Create a new chat session"""
        
        session = ChatSession(user_id=user.id)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_user_sessions(db: Session, user: User) -> list[ChatSession]:
        """Get all chat sessions for a user"""
        
        sessions = db.query(ChatSession)\
            .filter(ChatSession.user_id == user.id)\
            .order_by(ChatSession.updated_at.desc())\
            .all()
        return sessions
    
    @staticmethod
    def get_session_with_messages(db: Session, session_id: UUID, user: User):
        """Get a specific session with all its messages"""
        
        session = db.query(ChatSession)\
            .filter(ChatSession.id == session_id, ChatSession.user_id == user.id)\
            .first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        messages = db.query(ChatMessage)\
            .filter(ChatMessage.session_id == session_id)\
            .order_by(ChatMessage.timestamp.asc())\
            .all()
        
        return {"session": session, "messages": messages}
    
    @staticmethod
    async def send_message(db: Session, session_id: UUID, question: str, user: User) -> dict:
        """Send a message and get RAG response"""
        
        # Verify session belongs to user
        session = db.query(ChatSession)\
            .filter(ChatSession.id == session_id, ChatSession.user_id == user.id)\
            .first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Save user message
        user_message = ChatMessage(
            session_id=session_id,
            role="user",
            content=question
        )
        db.add(user_message)
        
        # Get chat history for context
        history = db.query(ChatMessage)\
            .filter(ChatMessage.session_id == session_id)\
            .order_by(ChatMessage.timestamp.asc())\
            .all()
        
        # Format history for RAG
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ]
        
        # Call RAG service
        rag_service = RAGService()
        answer = await rag_service.get_answer(question, chat_history)
        
        # Save assistant message
        assistant_message = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=answer
        )
        db.add(assistant_message)
        
        # Update session timestamp
        from datetime import datetime
        session.updated_at = datetime.utcnow()
        
        # Update session title with first question (if not set)
        if session.title == "New Conversation" and question:
            session.title = question[:50] + ("..." if len(question) > 50 else "")
        
        db.commit()
        
        return {
            "question": question,
            "answer": answer,
            "session_id": str(session_id)
        }
    
    @staticmethod
    def delete_session(db: Session, session_id: UUID, user: User):
        """Delete a chat session"""
        
        session = db.query(ChatSession)\
            .filter(ChatSession.id == session_id, ChatSession.user_id == user.id)\
            .first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        db.delete(session)
        db.commit()
        
        return {"message": "Session deleted successfully"}