from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone_number: Optional[str] = None
    school_name: Optional[str] = None
    province: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    school_name: Optional[str] = None
    province: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone_number: Optional[str] = None
    school_name: Optional[str] = None
    province: Optional[str] = None
    role: str
    subscription_tier: str
    is_verified: bool
    created_at: datetime
    first_login_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True