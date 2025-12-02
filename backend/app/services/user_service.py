from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth_service import get_password_hash
import uuid

def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> User | None:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)

    db_user = User(
        id=str(uuid.uuid4()),
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Authenticate a user by email and password"""
    from app.services.auth_service import verify_password

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user