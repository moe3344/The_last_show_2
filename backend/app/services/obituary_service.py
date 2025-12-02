from sqlalchemy.orm import Session
from app.models.obituary import Obituary
from app.schemas.obituary import ObituaryCreate
from typing import List, Optional
import uuid


def create_obituary(
    db: Session,
    user_id: str,
    obituary_data: ObituaryCreate,
    obituary_text: str,
    image_url: Optional[str] = None,
    audio_url: Optional[str] = None
) -> Obituary:
    """Create a new obituary"""
    
    db_obituary = Obituary(
        id=str(uuid.uuid4()),
        user_id=user_id,
        name=obituary_data.name,
        birth_date=obituary_data.birth_date,
        death_date=obituary_data.death_date,
        obituary_text=obituary_text,
        image_url=image_url,
        audio_url=audio_url,
        is_public=obituary_data.is_public
    )

    db.add(db_obituary)
    db.commit()
    db.refresh(db_obituary)

    return db_obituary

def get_obituaries(
    db: Session,
    user_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Obituary]:
    """Get all obituaries (optionally filtered by user)"""
    query = db.query(Obituary)

    if user_id:
        query = query.filter(Obituary.user_id == user_id)
    else:
        # Only show public obituaries if no user filter
        query = query.filter(Obituary.is_public == True)

    return query.order_by(Obituary.created_at.desc()).offset(skip).limit(limit).all()

def get_obituary_by_id(db: Session, obituary_id: str) -> Optional[Obituary]:
    """Get a single obituary by ID"""
    return db.query(Obituary).filter(Obituary.id == obituary_id).first()

def delete_obituary(db: Session, obituary_id: str, user_id: str) -> bool:
    """Delete an obituary (only if user owns it)"""
    obituary = db.query(Obituary).filter(
        Obituary.id == obituary_id,
        Obituary.user_id == user_id
    ).first()

    if not obituary:
        return False

    db.delete(obituary)
    db.commit()
    return True
