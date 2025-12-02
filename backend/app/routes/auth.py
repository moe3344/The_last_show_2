from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.user_service import create_user, get_user_by_email, authenticate_user
from app.services.auth_service import create_access_token
from app.dependencies import get_current_user
from app.models.user import User
from app.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
      """
      Register a new user
      """
      # Check if user already exists
      existing_user = get_user_by_email(db, email=user.email)
      if existing_user:
          raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail="Email already registered"
          )

      # Create new user
      db_user = create_user(db=db, user=user)

      return db_user

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
      """
      Login and get access token
      """
      # Authenticate user
      user = authenticate_user(db, email=user_credentials.email, password=user_credentials.password)

      if not user:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Incorrect email or password",
              headers={"WWW-Authenticate": "Bearer"},
          )

      # Create access token
      access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
      access_token = create_access_token(
          data={"sub": user.email},
          expires_delta=access_token_expires
      )

      return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
      """
      Get current logged-in user information
      This is a protected route - requires valid JWT token
      """
      return current_user