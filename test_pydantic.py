import enum
from pydantic import BaseModel, ConfigDict

class Role(str, enum.Enum):
    STUDENT = "student"

class UserResponse(BaseModel):
    role: str
    model_config = ConfigDict(from_attributes=True)

class User:
    def __init__(self):
        self.role = Role.STUDENT

u = User()
print("Validating:", UserResponse.model_validate(u))
