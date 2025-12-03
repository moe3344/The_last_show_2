"""
Unit tests for Obituary Service
"""
import pytest
from app.services.obituary_service import (
    create_obituary,
    get_obituaries,
    get_obituary_by_id,
    delete_obituary
)
from app.schemas.obituary import ObituaryCreate


class TestObituaryService:
    """Test suite for obituary service functions"""

    def test_create_obituary_success(self, db, test_user):
        """Test creating a new obituary successfully"""
        obituary_data = ObituaryCreate(
            name="Jane Smith",
            birth_date="1960-05-15",
            death_date="2024-02-20",
            is_public=True
        )
        obituary = create_obituary(
            db=db,
            user_id=test_user.id,
            obituary_data=obituary_data,
            obituary_text="A beloved teacher and mentor..."
        )

        assert obituary is not None
        assert obituary.name == "Jane Smith"
        assert obituary.user_id == test_user.id
        assert obituary.is_public is True
        assert obituary.id is not None

    def test_get_obituaries_public_only(self, db, test_user):
        """Test retrieving only public obituaries"""
        # Create public obituary
        public_obit = ObituaryCreate(
            name="Public Person",
            birth_date="1970-01-01",
            death_date="2024-01-01",
            is_public=True
        )
        create_obituary(db, test_user.id, public_obit, "Public content")

        # Create private obituary
        private_obit = ObituaryCreate(
            name="Private Person",
            birth_date="1975-01-01",
            death_date="2024-01-01",
            is_public=False
        )
        create_obituary(db, test_user.id, private_obit, "Private content")

        # Get obituaries without user_id filter shows only public
        obituaries = get_obituaries(db)

        assert len(obituaries) == 1
        assert obituaries[0].name == "Public Person"
        assert obituaries[0].is_public is True

    def test_get_obituaries_by_user(self, db, test_user):
        """Test retrieving obituaries by user ID"""
        obituary_data = ObituaryCreate(
            name="User's Obituary",
            birth_date="1980-01-01",
            death_date="2024-01-01",
            is_public=False
        )
        create_obituary(db, test_user.id, obituary_data, "User's content")

        obituaries = get_obituaries(db, user_id=test_user.id)

        assert len(obituaries) >= 1
        assert all(obit.user_id == test_user.id for obit in obituaries)

    def test_get_obituary_by_id_exists(self, db, test_obituary):
        """Test retrieving an existing obituary by ID"""
        obituary = get_obituary_by_id(db, test_obituary.id)

        assert obituary is not None
        assert obituary.id == test_obituary.id
        assert obituary.name == test_obituary.name

    def test_get_obituary_by_id_not_found(self, db):
        """Test retrieving a non-existent obituary by ID"""
        obituary = get_obituary_by_id(db, "non-existent-id")

        assert obituary is None

    def test_delete_obituary_success(self, db, test_user, test_obituary):
        """Test deleting an obituary successfully"""
        result = delete_obituary(db, test_obituary.id, test_user.id)

        assert result is True
        deleted_obituary = get_obituary_by_id(db, test_obituary.id)
        assert deleted_obituary is None

    def test_delete_obituary_wrong_user(self, db, test_user, test_obituary):
        """Test deleting an obituary with wrong user ID fails"""
        wrong_user_id = "wrong-user-id"
        result = delete_obituary(db, test_obituary.id, wrong_user_id)

        assert result is False
        obituary_still_exists = get_obituary_by_id(db, test_obituary.id)
        assert obituary_still_exists is not None
