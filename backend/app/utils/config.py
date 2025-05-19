import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # API settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Resume Skill Extractor"
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/resume_extractor")
    
    # File upload settings
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    
    model_config = {
        'case_sensitive': True
    }

# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
