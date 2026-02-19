from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.config import settings
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.utils.security import create_access_token, create_refresh_token

class GoogleAuthService:
    
    @staticmethod
    def verify_google_token(token: str) -> dict:
        """Verify Google ID token and return user info"""
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )
            
            # Verify issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            # Return user info from token
            return {
                'google_id': idinfo['sub'],
                'email': idinfo['email'],
                'full_name': idinfo.get('name', ''),
                'profile_picture': idinfo.get('picture', ''),
                'email_verified': idinfo.get('email_verified', False)
            }
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Google token: {str(e)}"
            )
    
    @staticmethod
    def authenticate_google_user(db: Session, token: str) -> TokenResponse:
        """Authenticate user with Google token"""
        
        # Verify Google token
        user_info = GoogleAuthService.verify_google_token(token)
        
        # Check if user exists by Google ID
        user = db.query(User).filter(User.google_id == user_info['google_id']).first()
        
        if not user:
            # Check if user exists by email (maybe registered with email/password)
            user = db.query(User).filter(User.email == user_info['email']).first()
            
            if user:
                # Link existing account with Google
                user.google_id = user_info['google_id']
                user.profile_picture = user_info['profile_picture']
                user.auth_provider = 'google'
                user.is_verified = True
            else:
                # Create new user
                user = User(
                    email=user_info['email'],
                    full_name=user_info['full_name'],
                    google_id=user_info['google_id'],
                    profile_picture=user_info['profile_picture'],
                    auth_provider='google',
                    is_verified=True,
                    password_hash=None  # No password for Google users
                )
                db.add(user)
            
            db.commit()
            db.refresh(user)
        
        # Create tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.from_orm(user)
        )