
import httpx
import base64
import logging
from typing import Optional
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)


async def upload_image_to_lambda(image_data: bytes, filename: str) -> Optional[str]:
      """
      Upload image to S3 via Lambda function

      Args:
          image_data: Image file bytes
          filename: Original filename

      Returns:
          S3 URL of uploaded image or None if failed
      """
      try:
          logger.info(f"Uploading image: {filename} ({len(image_data)} bytes)")

          # Encode image as base64
          image_base64 = base64.b64encode(image_data).decode('utf-8')

          async with httpx.AsyncClient(timeout=30.0) as client:
              response = await client.post(
                  settings.IMAGE_UPLOAD_LAMBDA_URL,
                  json={
                      "image": image_base64,
                      "filename": filename
                  }
              )

              if response.status_code == 200:
                  result = response.json()
                  image_url = result.get('image_url')
                  logger.info(f"Image uploaded successfully: {image_url}")
                  return image_url
              else:
                  logger.error(f"Image upload failed: {response.status_code} - {response.text}")
                  return None

      except httpx.TimeoutException:
          logger.error(f"Image upload timed out for {filename}")
          return None
      except Exception as e:
          logger.error(f"Error uploading image to Lambda: {e}", exc_info=True)
          return None


async def generate_tts_audio(text: str, obituary_id: str) -> Optional[str]:
      """
      Generate text-to-speech audio via Lambda function using Amazon Polly

      Args:
          text: Obituary text to convert to speech
          obituary_id: Unique ID for the obituary

      Returns:
          S3 URL of generated audio file or None if failed
      """
      try:
          logger.info(f"Generating TTS audio for obituary: {obituary_id}")
          logger.debug(f"Text length: {len(text)} characters")

          async with httpx.AsyncClient(timeout=60.0) as client:
              response = await client.post(
                  settings.TTS_LAMBDA_URL,
                  json={
                      "text": text,
                      "obituary_id": obituary_id
                  }
              )

              if response.status_code == 200:
                  result = response.json()
                  audio_url = result.get('audio_url')
                  logger.info(f"TTS audio generated successfully: {audio_url}")
                  return audio_url
              else:
                  logger.error(f"TTS generation failed: {response.status_code} - {response.text}")
                  return None

      except httpx.TimeoutException:
          logger.error(f"TTS generation timed out for obituary: {obituary_id}")
          return None
      except Exception as e:
          logger.error(f"Error generating TTS via Lambda: {e}", exc_info=True)
          return None
