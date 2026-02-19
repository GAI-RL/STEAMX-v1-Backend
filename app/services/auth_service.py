from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token

class AuthService:
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> dict:
        """Register a new user"""
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        new_user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            full_name=user_data.full_name
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {"message": "User registered successfully", "user_id": str(new_user.id)}
    
    @staticmethod
    def login(db: Session, credentials: LoginRequest) -> TokenResponse:
        """Authenticate user and return tokens"""
        
        # Find user
        user = db.query(User).filter(User.email == credentials.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        # Return response
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.from_orm(user)
        )