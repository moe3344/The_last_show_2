"""
Pytest configuration and fixtures for unit tests
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.models.obituary import Obituary
from app.services.auth_service import get_password_hash
import uuid

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db):
    """Create a test user"""
    user = User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        full_name="Test User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_obituary(db, test_user):
    """Create a test obituary"""
    obituary = Obituary(
        id=str(uuid.uuid4()),
        user_id=test_user.id,
        name="John Doe",
        birth_date="1950-01-01",
        death_date="2024-01-01",
        obituary_text="A loving father and friend...",
        is_public=True
    )
    db.add(obituary)
    db.commit()
    db.refresh(obituary)
    return obituary
