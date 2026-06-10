from pydantic import BaseModel
from uuid import UUID

class GradeResponse(BaseModel):
    id: UUID
    level: int
    display_name: str

    class Config:
        from_attributes = True