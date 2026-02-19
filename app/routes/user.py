from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile"""
    
    if update_data.full_name:
        current_user.full_name = update_data.full_name
    if update_data.email:
        # Check if email is already taken by another user
        existing_user = db.query(User).filter(
            User.email == update_data.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        current_user.email = update_data.email
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.get("/usage")
async def get_usage_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's usage statistics"""
    
    from app.models.chat import ChatSession, ChatMessage
    
    total_sessions = db.query(ChatSession)\
        .filter(ChatSession.user_id == current_user.id)\
        .count()
    
    total_messages = db.query(ChatMessage)\
        .join(ChatSession)\
        .filter(ChatSession.user_id == current_user.id)\
        .count()
    
    return {
        "total_sessions": total_sessions,
        "total_messages": total_messages,
        "subscription_tier": current_user.subscription_tier
    }

# ← NEW: Delete Account Endpoint
@router.delete("/account", status_code=status.HTTP_200_OK)
async def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete user account permanently"""
    
    # Delete user (cascades to chat_sessions, chat_messages, feedbacks)
    db.delete(current_user)
    db.commit()
    
    return {
        "message": "Account deleted successfully",
        "email": current_user.email
    }