from pydantic import BaseModel
from typing import Optional

class FeedbackCreate(BaseModel):
    rating: int  # 1-5
    comment: str | None = None

class ContactFormCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    topic: str
    institution: Optional[str] = None
    subject_line: Optional[str] = None
    message: str

class FeedbackResponse(BaseModel):
    message: str