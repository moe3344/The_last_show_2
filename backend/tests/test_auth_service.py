"""
Unit tests for authentication service
"""
import pytest
from datetime import timedelta
from app.services.auth_service import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)


@pytest.mark.unit
class TestPasswordHashing:
    """Test password hashing functionality"""

    def test_password_hash_and_verify(self):
        """Test password can be hashed and verified"""
        password = "mysecurepassword123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed) is True

    def test_wrong_password_fails_verification(self):
        """Test wrong password fails verification"""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_same_password_generates_different_hashes(self):
        """Test same password generates different hashes (salt)"""
        password = "samepassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


@pytest.mark.unit
class TestJWTTokens:
    """Test JWT token creation and decoding"""

    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {"sub": "user@example.com"}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self):
        """Test decoding valid JWT token"""
        email = "test@example.com"
        data = {"sub": email}
        token = create_access_token(data)

        decoded_email = decode_access_token(token)
        assert decoded_email == email

    def test_decode_invalid_token(self):
        """Test decoding invalid JWT token"""
        invalid_token = "invalid.token.here"
        result = decode_access_token(invalid_token)

        assert result is None

    def test_token_with_expiration(self):
        """Test token creation with custom expiration"""
        data = {"sub": "user@example.com"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)

        decoded_email = decode_access_token(token)
        assert decoded_email == "user@example.com"

    def test_decode_token_missing_subject(self):
        """Test decoding token without 'sub' claim"""
        data = {"user": "test@example.com"}  # Wrong key
        token = create_access_token(data)

        result = decode_access_token(token)
        assert result is None
