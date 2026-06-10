from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.chat_sessions import ChatSession, SessionStatus
from app.models.chat_messages import ChatMessage
from app.models.usage_daily import UsageDaily
from app.models.subject import Subject
from app.models.grade import Grade
from app.schemas.dashboard import (
    DashboardStatsResponse,
    RecentActivityResponse,
    RecentActivityItem,
    CalendarRangeResponse,
    DailyActivityItem,
    WeeklyActivityResponse
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStatsResponse)
async def get_stats(
    date_param: date = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get sessions and questions count for a specific date"""
    
    usage = db.query(UsageDaily).filter(
        UsageDaily.user_id == current_user.id,
        UsageDaily.date == date_param
    ).first()
    
    if usage:
        return DashboardStatsResponse(
            sessions=usage.sessions_created,
            questions=usage.qa_pairs_completed
        )
    
    return DashboardStatsResponse(sessions=0, questions=0)

@router.get("/recent-activity", response_model=RecentActivityResponse)
async def get_recent_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = 5
):
    """Get recent sessions with preview"""
    
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.status == SessionStatus.ACTIVE
    ).order_by(ChatSession.updated_at.desc()).limit(limit).all()
    
    activities = []
    for session in sessions:
        # Get last message preview (most recent Q&A)
        last_qa = db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id
        ).order_by(ChatMessage.created_at.desc()).first()
        
        # Get subject and grade info
        subject_name = None
        if session.subject_id:
            subject = db.query(Subject).filter(Subject.id == session.subject_id).first()
            subject_name = subject.name if subject else None
        
        grade_level = None
        if session.grade_id:
            grade = db.query(Grade).filter(Grade.id == session.grade_id).first()
            grade_level = grade.level if grade else None
        
        activities.append(RecentActivityItem(
            session_id=session.id,
            title=session.title,
            subject_name=subject_name,
            grade_level=grade_level,
            last_message_preview=last_qa.prompt[:100] if last_qa else "",
            qa_pairs_count=session.total_qa_pairs,
            updated_at=session.updated_at
        ))
    
    return RecentActivityResponse(activities=activities)

@router.get("/calendar-range", response_model=CalendarRangeResponse)
async def get_calendar_range(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get first login date and today for calendar initialization"""
    
    first_login = current_user.first_login_at.date() if current_user.first_login_at else date.today()
    
    return CalendarRangeResponse(
        first_login_at=first_login,
        today=date.today()
    )

@router.get("/weekly-activity", response_model=WeeklyActivityResponse)
async def get_weekly_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily sessions and questions count for the last 7 days"""
    today = date.today()
    activity = []
    
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        usage = db.query(UsageDaily).filter(
            UsageDaily.user_id == current_user.id,
            UsageDaily.date == day
        ).first()
        
        activity.append(DailyActivityItem(
            date=day.strftime("%Y-%m-%d"),
            sessions=usage.sessions_created if usage else 0,
            questions=usage.qa_pairs_completed if usage else 0
        ))
        
    return WeeklyActivityResponse(activity=activity)