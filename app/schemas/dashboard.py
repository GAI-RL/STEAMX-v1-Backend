from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class DashboardStatsResponse(BaseModel):
    sessions: int
    questions: int

class RecentActivityItem(BaseModel):
    session_id: UUID
    title: str
    subject_name: Optional[str] = None
    grade_level: Optional[int] = None
    last_message_preview: str
    qa_pairs_count: int
    updated_at: datetime

class RecentActivityResponse(BaseModel):
    activities: list[RecentActivityItem]

class CalendarRangeResponse(BaseModel):
    first_login_at: date
    today: date

class DailyActivityItem(BaseModel):
    date: str
    sessions: int
    questions: int

class WeeklyActivityResponse(BaseModel):
    activity: list[DailyActivityItem]