from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class SubjectResponse(BaseModel):
    id: UUID
    name: str
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True