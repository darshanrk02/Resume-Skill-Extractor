# Import models to make them available when importing from app.models
from .database import Base, engine, SessionLocal, init_db, get_db
from .resume import ResumeData

# Import models after database initialization to avoid circular imports
from .sql_models import Resume, ContactInfo, Skill, Education, Experience, Project

# Initialize database tables
init_db()

__all__ = [
    'Base',
    'engine',
    'SessionLocal',
    'init_db',
    'get_db',
    'ResumeData',
    'Resume',
    'ContactInfo',
    'Skill',
    'Education',
    'Experience',
    'Project'
]
