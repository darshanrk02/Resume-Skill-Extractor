from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, schemas

def get_resume_by_id(db: Session, resume_id: int):
    """Get a resume by ID"""
    return db.query(models.Resume).filter(models.Resume.id == resume_id).first()

def get_all_resumes(db: Session, skip: int = 0, limit: int = 100):
    """Get all resumes with pagination"""
    return db.query(models.Resume).offset(skip).limit(limit).all()

def create_resume(db: Session, resume: schemas.ResumeCreate):
    """Create a new resume"""
    db_resume = models.Resume(**resume.dict())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume
