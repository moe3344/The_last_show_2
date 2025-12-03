"""
Unit tests for User Service
"""
import pytest
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    authenticate_user
)
from app.schemas.user import UserCreate


class TestUserService:
    """Test suite for user service functions"""

    def test_create_user_success(self, db):
        """Test creating a new user successfully"""
        user_data = UserCreate(
            email="newuser@example.com",
            password="securepassword123",
            full_name="New User"
        )
        user = create_user(db, user_data)

        assert user is not None
        assert user.email == "newuser@example.com"
        assert user.full_name == "New User"
        assert user.hashed_password != "securepassword123"  # Password should be hashed
        assert user.id is not None

    def test_create_user_duplicate_email(self, db, test_user):
        """Test creating a user with duplicate email raises IntegrityError"""
        from sqlalchemy.exc import IntegrityError

        user_data = UserCreate(
            email=test_user.email,
            password="password123",
            full_name="Duplicate User"
        )

        with pytest.raises(IntegrityError):
            create_user(db, user_data)

    def test_get_user_by_email_exists(self, db, test_user):
        """Test retrieving an existing user by email"""
        user = get_user_by_email(db, test_user.email)

        assert user is not None
        assert user.email == test_user.email
        assert user.id == test_user.id

    def test_get_user_by_email_not_found(self, db):
        """Test retrieving a non-existent user by email"""
        user = get_user_by_email(db, "nonexistent@example.com")

        assert user is None

    def test_get_user_by_id_exists(self, db, test_user):
        """Test retrieving an existing user by ID"""
        user = get_user_by_id(db, test_user.id)

        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_user_by_id_not_found(self, db):
        """Test retrieving a non-existent user by ID"""
        user = get_user_by_id(db, "non-existent-id")

        assert user is None

    def test_authenticate_user_success(self, db, test_user):
        """Test authenticating a user with correct credentials"""
        user = authenticate_user(db, test_user.email, "testpassword123")

        assert user is not None
        assert user.email == test_user.email

    def test_authenticate_user_wrong_password(self, db, test_user):
        """Test authentication fails with wrong password"""
        user = authenticate_user(db, test_user.email, "wrongpassword")

        assert user is None

    def test_authenticate_user_nonexistent_email(self, db):
        """Test authentication fails with non-existent email"""
        user = authenticate_user(db, "nonexistent@example.com", "password123")

        assert user is None
