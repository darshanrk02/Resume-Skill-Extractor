import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload

from app.models.database import get_db
from app.models.resume import (
    ContactInfo,
    Education as PydanticEducation,
    Experience as PydanticExperience,
    Project as PydanticProject,
    ResumeData,
)
from app.models.sql_models import (
    ContactInfo as DBContactInfo,
    Education as DBEducation,
    Experience as DBExperience,
    Project as DBProject,
    Resume as DBResume,
    Skill as DBSkill,
)
from app.services.resume_extractor import ResumeExtractor

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["resume"])

# Configure upload directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

def allowed_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/resume/upload", response_model=ResumeData)
async def upload_resume(
    file: UploadFile = File(..., description="Resume file (PDF, DOC, or DOCX)"),
    db: Session = Depends(get_db)
) -> ResumeData:
    """
    Upload a resume file and extract information from it.
    
    Supported formats: PDF, DOC, DOCX
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    # Validate file type
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate a unique filename to avoid conflicts
    file_ext = Path(file.filename).suffix.lower()
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"resume_{timestamp}{file_ext}"
    file_path = UPLOAD_DIR / safe_filename
    
    try:
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract information from the resume
        try:
            logger.info(f"Processing resume: {file.filename}")
            extractor = ResumeExtractor(str(file_path))
            extracted_data = extractor.extract_all()
            
            # Extract just the skill names from the skills objects and format them as expected by frontend
            skills_data = extracted_data.get("skills", [])
            formatted_skills = []
            if isinstance(skills_data, list):
                for skill in skills_data:
                    if isinstance(skill, dict) and "name" in skill:
                        formatted_skills.append({"name": skill["name"]})
                    elif isinstance(skill, str):
                        formatted_skills.append({"name": skill})
            
            # Convert to Pydantic model
            resume_data = ResumeData(
                contact_info=ContactInfo(**extracted_data.get("contact_info", {})),
                summary=extracted_data.get("summary"),
                skills=formatted_skills,
                education=[
                    PydanticEducation(**edu) for edu in extracted_data.get("education", [])
                ],
                experience=[
                    PydanticExperience(**exp) for exp in extracted_data.get("experience", [])
                ],
                projects=[
                    PydanticProject(
                        name=proj["name"],
                        description=proj["description"],
                        technologies=[tech.strip() for tech in proj.get("technologies", "").split(",")] if proj.get("technologies") else [],
                        start_date=proj.get("start_date"),
                        end_date=proj.get("end_date"),
                        url=proj.get("url")
                    ) for proj in extracted_data.get("projects", [])
                ],
                certifications=extracted_data.get("certifications", []),
                languages=extracted_data.get("languages", []),
                raw_text=extracted_data.get("raw_text"),
                file_name=file.filename,
                file_type=file_ext.lstrip("."),
                file_size=os.path.getsize(file_path)
            )
            
            return resume_data
            
        except ValueError as ve:
            logger.error(f"Error processing resume: {str(ve)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )
            
        except Exception as e:
            logger.error(f"Error extracting resume data: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing the resume. Please try again."
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, 
            detail=f"Error processing file upload: {str(e)}")
            
    finally:
        # Clean up the uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing temporary file {file_path}: {e}")

@router.post("/resume/save", status_code=status.HTTP_201_CREATED)
async def save_resume(
    resume_data: ResumeData,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Save the extracted resume data to the database.
    
    This endpoint accepts a ResumeData object and stores it in the database.
    """
    try:
        # Start a transaction
        with db.begin():
            # Create Resume record
            db_resume = DBResume(
                filename=resume_data.file_name or "resume.pdf",
                upload_date=resume_data.created_at or datetime.utcnow()
            )
            db.add(db_resume)
            db.flush()  # To get the resume.id
            
            # Create ContactInfo record if contact info exists
            if resume_data.contact_info:
                contact_info = DBContactInfo(
                    resume_id=db_resume.id,
                    name=resume_data.contact_info.name,
                    email=resume_data.contact_info.email,
                    phone=resume_data.contact_info.phone,
                    location=resume_data.contact_info.location,
                    linkedin=resume_data.contact_info.linkedin,
                    github=resume_data.contact_info.github,
                    portfolio=resume_data.contact_info.portfolio
                )
                db.add(contact_info)
            
            # Create Skills records
            for skill_name in resume_data.skills:
                skill = DBSkill(
                    resume_id=db_resume.id,
                    name=skill_name,
                    # You might want to add skill categorization here
                    category=None
                )
                db.add(skill)
            
            # Create Education records
            for edu in resume_data.education:
                education = DBEducation(
                    resume_id=db_resume.id,
                    institution=edu.institution,
                    degree=edu.degree,
                    field_of_study=edu.field_of_study,
                    start_date=edu.start_date,
                    end_date=edu.end_date,
                    gpa=edu.gpa
                )
                db.add(education)
            
            # Create Experience records
            for exp in resume_data.experience:
                experience = DBExperience(
                    resume_id=db_resume.id,
                    company=exp.company,
                    position=exp.position,
                    location=exp.location,
                    start_date=exp.start_date,
                    end_date=exp.end_date,
                    current=exp.current,
                    description=exp.description
                )
                db.add(experience)
            
            # Create Project records
            for proj in resume_data.projects:
                project = DBProject(
                    resume_id=db_resume.id,
                    name=proj.name,
                    description=proj.description,
                    technologies=",".join(proj.technologies) if proj.technologies else None,
                    start_date=proj.start_date,
                    end_date=proj.end_date,
                    url=proj.url
                )
                db.add(project)
            
        logger.info(f"Successfully saved resume with ID: {db_resume.id}")
        return {
            "message": "Resume saved successfully",
            "resume_id": db_resume.id,
            "file_name": resume_data.file_name,
            "upload_date": db_resume.upload_date.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error saving resume: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving the resume. Please try again."
        )

@router.get("/resumes/{resume_id}", response_model=ResumeData)
async def get_resume(
    resume_id: int,
    db: Session = Depends(get_db)
) -> ResumeData:
    """
    Get a resume by ID with all its related information.
    
    Returns a fully populated ResumeData object with all related entities.
    """
    try:
        # Get the resume with all relationships loaded
        db_resume = db.query(DBResume).options(
            joinedload(DBResume.contact_info),
            joinedload(DBResume.skills),
            joinedload(DBResume.education),
            joinedload(DBResume.experience),
            joinedload(DBResume.projects)
        ).filter(DBResume.id == resume_id).first()
        
        if not db_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resume with ID {resume_id} not found"
            )
        
        # Convert to Pydantic model
        return ResumeData.from_db_model(db_resume)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving resume {resume_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the resume. Please try again."
        )

@router.get("/resumes", response_model=List[ResumeData])
async def get_all_resumes(
    db: Session = Depends(get_db)
) -> List[ResumeData]:
    """
    Get all resumes (summary information only)
    """
    try:
        # Query all resumes
        db_resumes = db.query(DBResume).options(
            joinedload(DBResume.contact_info),
            joinedload(DBResume.skills),
            joinedload(DBResume.education),
            joinedload(DBResume.experience),
            joinedload(DBResume.projects)
        ).order_by(DBResume.upload_date.desc()).all()
        
        return [ResumeData.from_db_model(db_resume) for db_resume in db_resumes]
    
    except Exception as e:
        logger.error(f"Error retrieving resumes: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the resumes. Please try again."
        )

@router.delete("/resumes/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a resume and all its related information.
    
    This is a hard delete operation and cannot be undone.
    """
    try:
        with db.begin():
            # Find the resume
            db_resume = db.query(DBResume).filter(DBResume.id == resume_id).first()
            
            if not db_resume:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Resume with ID {resume_id} not found"
                )
            
            # Delete the resume (SQLAlchemy cascade should handle related records)
            db.delete(db_resume)
            
            # If you need to handle file deletion:
            # if db_resume.file_path and os.path.exists(db_resume.file_path):
            #     try:
            #         os.remove(db_resume.file_path)
            #     except OSError as e:
            #         logger.warning(f"Failed to delete file {db_resume.file_path}: {str(e)}")
            
        logger.info(f"Successfully deleted resume with ID: {resume_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting resume {resume_id}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the resume. Please try again."
        )
