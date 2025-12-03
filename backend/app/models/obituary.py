from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import uuid

class Obituary(Base):
    __tablename__ = "obituaries"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)

    # Person details
    name = Column(String, nullable=False)
    birth_date = Column(String, nullable=False) 
    death_date = Column(String, nullable=False) 

    # Generated content
    obituary_text = Column(Text, nullable=False)  

    # Media URLs
    image_url = Column(String, nullable=True) 
    audio_url = Column(String, nullable=True)  #

    # Visibility
    is_public = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
