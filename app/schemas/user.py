from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

# Request schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None

# Response schemas
class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    created_at: datetime
    subscription_tier: str
    
    class Config:
        from_attributes = True