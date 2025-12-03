"""
Unit tests for obituary service
"""
import pytest
from app.services.obituary_service import (
    create_obituary,
    get_obituaries,
    get_obituary_by_id,
    delete_obituary
)
from app.schemas.obituary import ObituaryCreate


@pytest.mark.unit
class TestObituaryService:
    """Test obituary service functions"""

    def test_create_obituary(self, db, test_user):
        """Test creating a new obituary"""
        obituary_data = ObituaryCreate(
            name="John Doe",
            birth_date="1950-01-01",
            death_date="2024-01-01",
            is_public=True
        )

        obituary = create_obituary(
            db=db,
            user_id=test_user.id,
            obituary_data=obituary_data,
            obituary_text="A loving tribute...",
            image_url="https://example.com/image.jpg",
            audio_url="https://example.com/audio.mp3"
        )

        assert obituary.id is not None
        assert obituary.name == "John Doe"
        assert obituary.birth_date == "1950-01-01"
        assert obituary.death_date == "2024-01-01"
        assert obituary.obituary_text == "A loving tribute..."
        assert obituary.user_id == test_user.id

    def test_get_obituaries_public_only(self, db, test_user):
        """Test retrieving only public obituaries"""
        # Create public obituary
        public_data = ObituaryCreate(
            name="Public Person",
            birth_date="1960-01-01",
            death_date="2024-01-01",
            is_public=True
        )
        create_obituary(db, test_user.id, public_data, "Public text")

        # Create private obituary
        private_data = ObituaryCreate(
            name="Private Person",
            birth_date="1965-01-01",
            death_date="2024-01-01",
            is_public=False
        )
        create_obituary(db, test_user.id, private_data, "Private text")

        # Get all public obituaries
        obituaries = get_obituaries(db)

        assert len(obituaries) == 1
        assert obituaries[0].name == "Public Person"

    def test_get_obituaries_by_user(self, db, test_user):
        """Test retrieving obituaries by user ID"""
        obituary_data = ObituaryCreate(
            name="User Obituary",
            birth_date="1970-01-01",
            death_date="2024-01-01",
            is_public=False
        )
        create_obituary(db, test_user.id, obituary_data, "User's obituary")

        obituaries = get_obituaries(db, user_id=test_user.id)

        assert len(obituaries) == 1
        assert obituaries[0].user_id == test_user.id

    def test_get_obituary_by_id(self, db, test_user):
        """Test retrieving obituary by ID"""
        obituary_data = ObituaryCreate(
            name="Test Person",
            birth_date="1975-01-01",
            death_date="2024-01-01",
            is_public=True
        )
        created = create_obituary(db, test_user.id, obituary_data, "Test text")

        obituary = get_obituary_by_id(db, created.id)

        assert obituary is not None
        assert obituary.id == created.id
        assert obituary.name == "Test Person"

    def test_get_obituary_by_id_not_found(self, db):
        """Test retrieving non-existent obituary"""
        obituary = get_obituary_by_id(db, "non-existent-id")

        assert obituary is None

    def test_delete_obituary_success(self, db, test_user):
        """Test successfully deleting an obituary"""
        obituary_data = ObituaryCreate(
            name="Delete Me",
            birth_date="1980-01-01",
            death_date="2024-01-01",
            is_public=True
        )
        obituary = create_obituary(db, test_user.id, obituary_data, "To be deleted")

        result = delete_obituary(db, obituary.id, test_user.id)

        assert result is True
        assert get_obituary_by_id(db, obituary.id) is None

    def test_delete_obituary_wrong_user(self, db, test_user):
        """Test deleting obituary with wrong user ID fails"""
        obituary_data = ObituaryCreate(
            name="Protected",
            birth_date="1985-01-01",
            death_date="2024-01-01",
            is_public=True
        )
        obituary = create_obituary(db, test_user.id, obituary_data, "Protected")

        result = delete_obituary(db, obituary.id, "wrong-user-id")

        assert result is False
        assert get_obituary_by_id(db, obituary.id) is not None
