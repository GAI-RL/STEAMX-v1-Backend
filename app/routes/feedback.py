from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.feedback import Feedback, FeedbackType
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, ContactFormCreate

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
        comment=feedback_data.comment,
        feedback_type=FeedbackType.GENERAL
    )
    
    db.add(feedback)
    db.commit()
    
    return FeedbackResponse(message="Feedback submitted successfully")

@router.post("/contact", response_model=FeedbackResponse)
async def submit_contact_form(
    contact_data: ContactFormCreate,
    db: Session = Depends(get_db)
):
    """Submit a public contact form message"""
    
    feedback = Feedback(
        feedback_type=FeedbackType.CONTACT_FORM,
        first_name=contact_data.first_name,
        last_name=contact_data.last_name,
        email=contact_data.email,
        phone_number=contact_data.phone_number,
        topic=contact_data.topic,
        institution=contact_data.institution,
        subject_line=contact_data.subject_line,
        message=contact_data.message
    )
    
    db.add(feedback)
    db.commit()
    
    return FeedbackResponse(message="Contact form submitted successfully")