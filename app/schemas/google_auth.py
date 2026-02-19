from pydantic import BaseModel
from app.schemas.auth import TokenResponse

class GoogleAuthRequest(BaseModel):
    token: str  # Google ID token from frontend

class GoogleAuthResponse(TokenResponse):
    pass  # Same as regular auth response