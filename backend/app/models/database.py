from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment or use default (SQLite for easier setup)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resume_extractor.db")

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def init_db():
    # Import models here to ensure they are registered with SQLAlchemy
    from . import sql_models  # noqa: F401
    # Create all tables
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency that provides a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
