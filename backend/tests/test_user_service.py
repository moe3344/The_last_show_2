"""
Unit tests for user service
"""
import pytest
from app.services.user_service import (
    get_user_by_email,
    get_user_by_id,
    create_user,
    authenticate_user
)
from app.schemas.user import UserCreate
from app.services.auth_service import get_password_hash


@pytest.mark.unit
class TestUserService:
    """Test user service functions"""

    def test_create_user(self, db):
        """Test creating a new user"""
        user_data = UserCreate(
            email="newuser@example.com",
            password="password123",
            full_name="New User"
        )

        user = create_user(db, user_data)

        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.full_name == "New User"
        assert user.hashed_password != "password123"

    def test_get_user_by_email(self, db, test_user):
        """Test retrieving user by email"""
        user = get_user_by_email(db, test_user.email)

        assert user is not None
        assert user.email == test_user.email
        assert user.id == test_user.id

    def test_get_user_by_email_not_found(self, db):
        """Test retrieving non-existent user by email"""
        user = get_user_by_email(db, "nonexistent@example.com")

        assert user is None

    def test_get_user_by_id(self, db, test_user):
        """Test retrieving user by ID"""
        user = get_user_by_id(db, test_user.id)

        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_user_by_id_not_found(self, db):
        """Test retrieving non-existent user by ID"""
        user = get_user_by_id(db, "non-existent-id")

        assert user is None

    def test_authenticate_user_success(self, db, test_user):
        """Test successful user authentication"""
        user = authenticate_user(db, "test@example.com", "testpassword123")

        assert user is not None
        assert user.email == test_user.email

    def test_authenticate_user_wrong_password(self, db, test_user):
        """Test authentication with wrong password"""
        user = authenticate_user(db, "test@example.com", "wrongpassword")

        assert user is None

    def test_authenticate_user_nonexistent_email(self, db):
        """Test authentication with non-existent email"""
        user = authenticate_user(db, "nonexistent@example.com", "password")

        assert user is None
