
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import decode_access_token
from app.services.user_service import get_user_by_email
from app.models.user import User

# Change this from OAuth2PasswordBearer to HTTPBearer
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract token from credentials
    token = credentials.credentials

    # Decode token
    email = decode_access_token(token)

    if email is None:
        raise credentials_exception

    # Get user from database
    user = get_user_by_email(db, email=email)

    if user is None:
        raise credentials_exception

    return user
