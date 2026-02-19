from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("", response_model=FeedbackResponse)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit user feedback"""
    
    feedback = Feedback(
        user_id=current_user.id,
        rating=feedback_data.rating,
        comment=feedback_data.comment
    )
    
    db.add(feedback)
    db.commit()
    
    return FeedbackResponse(message="Feedback submitted successfully")