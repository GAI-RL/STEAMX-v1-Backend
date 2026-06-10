from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.schemas.user import UserCreate
from app.schemas.google_auth import GoogleAuthRequest, GoogleAuthResponse
from app.services.auth_service import AuthService
from app.services.google_auth_service import GoogleAuthService
from app.utils.security import decode_token, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return AuthService.register_user(db, user_data)

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login and get access tokens"""
    
    result = AuthService.login(db, credentials)
    
    # Update login timestamps
    from app.models.user import User
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if user:
        if user.first_login_at is None:
            user.first_login_at = datetime.utcnow()
        user.last_login_at = datetime.utcnow()
        db.commit()
    
    return result

@router.post("/google", response_model=GoogleAuthResponse)
async def google_auth(
    request: GoogleAuthRequest, 
    db: Session = Depends(get_db)
):
    """Authenticate with Google"""
    result = GoogleAuthService.authenticate_google_user(db, request.token)
    
    # Update login timestamps
    from app.models.user import User
    user = db.query(User).filter(User.email == result.user.email).first()
    
    if user:
        if user.first_login_at is None:
            user.first_login_at = datetime.utcnow()
        user.last_login_at = datetime.utcnow()
        db.commit()
    
    return result

@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    
    payload = decode_token(request.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    new_access_token = create_access_token({"sub": user_id})
    
    return {"access_token": new_access_token}

@router.post("/logout")
async def logout():
    """Logout (client-side token removal)"""
    return {"message": "Logged out successfully"}