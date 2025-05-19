import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List
from pydantic import ConfigDict

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Resume Skill Extractor"
    PORT: int = 8000  # Added to match .env
    
    # CORS settings - store as string and parse in the app
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001,http://localhost:8000"
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list of origins"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./resume_extractor.db")
    
    # MongoDB settings
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "resume_extractor")
    
    # File upload settings
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    
    # Model settings
    SENTENCE_TRANSFORMER_MODEL: str = "paraphrase-MiniLM-L6-v2"

    # Pydantic v2 style configuration
    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding='utf-8',
        extra="allow"  # Allow extra fields from environment variables
    )

# Create settings instance
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
