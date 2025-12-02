from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ObituaryCreate(BaseModel):
    name: str
    birth_date: str  # "YYYY-MM-DD"
    death_date: str  # "YYYY-MM-DD"
    is_public: bool = False
    image: Optional[str] = None  # Base64 encoded image or will be file upload
class ObituaryResponse(BaseModel):
    id: str
    user_id: str
    name: str
    birth_date: str
    death_date: str
    obituary_text: str
    image_url: Optional[str]
    audio_url: Optional[str]
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True
class ObituaryListResponse(BaseModel):
    obituaries: list[ObituaryResponse]
    total: int