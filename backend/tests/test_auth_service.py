"""
Unit tests for Authentication Service
"""

from datetime import timedelta
from app.services.auth_service import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)


class TestPasswordHashing:
    """Test suite for password hashing functions"""

    def test_password_hash_and_verify(self):
        """Test that password can be hashed and verified"""
        password = "mysecretpassword"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed) is True

    def test_wrong_password_fails_verification(self):
        """Test that wrong password fails verification"""
        password = "correctpassword"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_same_password_generates_different_hashes(self):
        """Test that same password generates different hashes (salt)"""
        password = "testpassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokens:
    """Test suite for JWT token functions"""

    def test_create_access_token(self):
        """Test creating an access token"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self):
        """Test decoding a valid token"""
        email = "test@example.com"
        data = {"sub": email}
        token = create_access_token(data)

        decoded_email = decode_access_token(token)

        assert decoded_email == email

    def test_decode_invalid_token(self):
        """Test decoding an invalid token returns None"""
        invalid_token = "invalid.token.here"
        decoded_email = decode_access_token(invalid_token)

        assert decoded_email is None

    def test_token_with_expiration(self):
        """Test creating a token with custom expiration"""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)

        assert token is not None
        decoded_email = decode_access_token(token)
        assert decoded_email == "test@example.com"

    def test_decode_token_missing_subject(self):
        """Test decoding a token without 'sub' claim returns None"""
        data = {"user": "test@example.com"}  # Wrong key
        token = create_access_token(data)

        decoded_email = decode_access_token(token)

        assert decoded_email is None
