from pydantic import BaseModel
from app.schemas.user import UserResponse

class GoogleAuthRequest(BaseModel):
    token: str  # Google ID token from frontend

class GoogleAuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse