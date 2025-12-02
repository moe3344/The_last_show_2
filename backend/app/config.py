from pydantic_settings import BaseSettings




class Settings(BaseSettings):
      DATABASE_URL: str
      SECRET_KEY: str
      ALGORITHM: str = "HS256"
      ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
      DEBUG: bool = False

      
      GROQ_API_KEY: str 
      IMAGE_UPLOAD_LAMBDA_URL: str
      TTS_LAMBDA_URL: str

      class Config:
          env_file = ".env"

settings = Settings()
