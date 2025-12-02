from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.encoders import jsonable_encoder
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.obituary import ObituaryCreate, ObituaryResponse, ObituaryListResponse
from app.services import obituary_service
from app.services.ai_service import generate_obituary_text
from app.services.lambda_service import upload_image_to_lambda, generate_tts_audio
import logging

logger = logging.getLogger("uvicorn")

router = APIRouter()


@router.post("/", response_model=ObituaryResponse, status_code=status.HTTP_201_CREATED)
async def create_obituary(
    name: str = Form(...),
    birth_date: str = Form(...),
    death_date: str = Form(...),
    is_public: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new obituary with AI-generated text, optional image, and TTS audio.
    Works with multipart/form-data.
    """
    logger.info("📥 Incoming obituary creation request")
    logger.info(f"name={name!r}, birth_date={birth_date!r}, death_date={death_date!r}, is_public={is_public!r}, image={image.filename if image else None}")
    # Log incoming data
    logger.info("📥 Incoming obituary creation request")
    logger.info(f"name: {name!r}")
    logger.info(f"birth_date: {birth_date!r}")
    logger.info(f"death_date: {death_date!r}")
    logger.info(f"is_public: {is_public!r}")
    logger.info(f"image: {image.filename if image else None}")

    # Generate obituary text using AI
    obituary_text = generate_obituary_text(
        name=name,
        birth_date=birth_date,
        death_date=death_date
    )

    # Upload image if provided
    image_url = None
    if image:
        logger.info(f"📤 Uploading image: {image.filename}")
        image_data = await image.read()
        logger.info(f"📦 Image size: {len(image_data)} bytes")
        image_url = await upload_image_to_lambda(image_data, image.filename)
        if image_url:
            logger.info(f"✅ Image uploaded successfully: {image_url}")
        else:
            logger.error(f"❌ Image upload failed for {image.filename}")

    # Create obituary data object
    obituary_data = ObituaryCreate(
        name=name,
        birth_date=birth_date,
        death_date=death_date,
        is_public=is_public
    )

    # Create obituary in database (without audio_url yet)
    obituary = obituary_service.create_obituary(
        db=db,
        user_id=current_user.id,
        obituary_data=obituary_data,
        obituary_text=obituary_text,
        image_url=image_url,
        audio_url=None
    )

    # Generate TTS audio in background
    audio_url = await generate_tts_audio(obituary_text, obituary.id)

    # Update obituary with audio URL
    if audio_url:
        obituary.audio_url = audio_url
        db.commit()
        db.refresh(obituary)

    logger.info(f"✅ Obituary created with ID: {obituary.id}")

   
    return jsonable_encoder(obituary)

@router.get("/", response_model=ObituaryListResponse)
def get_obituaries(
      skip: int = 0,
      limit: int = 100,
      db: Session = Depends(get_db)
  ):
      """
      Get all public obituaries
      """
      obituaries = obituary_service.get_obituaries(db=db, skip=skip, limit=limit)
      return {
          "obituaries": obituaries,
          "total": len(obituaries)
      }


@router.get("/my-obituaries", response_model=ObituaryListResponse)
def get_my_obituaries(
      current_user: User = Depends(get_current_user),
      db: Session = Depends(get_db)
  ):
      """
      Get current user's obituaries (protected route)
      """
      obituaries = obituary_service.get_obituaries(db=db, user_id=current_user.id)
      return {
          "obituaries": obituaries,
          "total": len(obituaries)
      }


@router.get("/{obituary_id}", response_model=ObituaryResponse)
def get_obituary(
      obituary_id: str,
      db: Session = Depends(get_db)
  ):
      """
      Get a single obituary by ID
      """
      obituary = obituary_service.get_obituary_by_id(db=db, obituary_id=obituary_id)

      if not obituary:
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="Obituary not found"
          )

      return obituary


@router.delete("/{obituary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_obituary(
      obituary_id: str,
      current_user: User = Depends(get_current_user),
      db: Session = Depends(get_db)
  ):
      """
      Delete an obituary (protected route - only owner can delete)
      """
      success = obituary_service.delete_obituary(
          db=db,
          obituary_id=obituary_id,
          user_id=current_user.id
      )

      if not success:
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="Obituary not found or you don't have permission to delete it"
          )

      return None
