import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from bson import ObjectId

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

from app.models.mongodb import get_resume_collection
from app.models.resume import ResumeData
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
    file: UploadFile = File(..., description="Resume file (PDF, DOC, or DOCX)")
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
                contact_info=extracted_data.get("contact_info", {}),
                summary=extracted_data.get("summary"),
                skills=formatted_skills,
                education=extracted_data.get("education", []),
                experience=extracted_data.get("experience", []),
                projects=extracted_data.get("projects", []),
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
    resume_data: ResumeData
) -> Dict[str, Any]:
    """
    Save the extracted resume data to MongoDB.
    
    This endpoint accepts a ResumeData object and stores it in the database.
    """
    try:
        # Get the resume collection
        resumes_collection = get_resume_collection()
        
        # Convert Pydantic model to dict for MongoDB
        resume_dict = resume_data.dict()
        
        # Add timestamps
        resume_dict["created_at"] = datetime.utcnow()
        resume_dict["updated_at"] = datetime.utcnow()
        
        # Insert into MongoDB
        result = resumes_collection.insert_one(resume_dict)
        
        logger.info(f"Successfully saved resume with ID: {result.inserted_id}")
        return {
            "message": "Resume saved successfully",
            "resume_id": str(result.inserted_id),
            "file_name": resume_data.file_name,
            "upload_date": resume_dict["created_at"].isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error saving resume: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while saving the resume: {str(e)}"
        )

@router.get("/resumes/{resume_id}", response_model=ResumeData)
async def get_resume(
    resume_id: str
) -> ResumeData:
    """
    Get a resume by ID with all its related information.
    
    Returns a fully populated ResumeData object.
    """
    try:
        # Get the resume collection
        resumes_collection = get_resume_collection()
        
        # Query the resume by ID
        try:
            object_id = ObjectId(resume_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid resume ID format"
            )
            
        resume = resumes_collection.find_one({"_id": object_id})
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resume with ID {resume_id} not found"
            )
        
        # Convert MongoDB document to ResumeData
        # Remove MongoDB _id field
        resume.pop("_id", None)
        resume.pop("created_at", None)
        resume.pop("updated_at", None)
        
        # Return as Pydantic model
        return ResumeData(**resume)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving resume {resume_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the resume. Please try again."
        )

@router.get("/resumes", response_model=List[ResumeData])
async def get_all_resumes() -> List[ResumeData]:
    """
    Get all resumes (summary information only)
    """
    try:
        # Get the resume collection
        resumes_collection = get_resume_collection()
        
        # Query all resumes, sorted by creation date
        resumes = list(resumes_collection.find().sort("created_at", -1))
        
        # Convert MongoDB documents to ResumeData list
        resume_list = []
        for resume in resumes:
            # Remove MongoDB _id field and timestamps
            resume.pop("_id", None)
            resume.pop("created_at", None)
            resume.pop("updated_at", None)
            
            # Convert to Pydantic model
            resume_list.append(ResumeData(**resume))
        
        return resume_list
    
    except Exception as e:
        logger.error(f"Error retrieving resumes: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the resumes. Please try again."
        )

@router.delete("/resumes/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str
) -> None:
    """
    Delete a resume by ID.
    
    This is a hard delete operation and cannot be undone.
    """
    try:
        # Get the resume collection
        resumes_collection = get_resume_collection()
        
        # Convert string ID to ObjectId
        try:
            object_id = ObjectId(resume_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid resume ID format"
            )
            
        # Delete the resume
        result = resumes_collection.delete_one({"_id": object_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resume with ID {resume_id} not found"
            )
            
        logger.info(f"Successfully deleted resume with ID: {resume_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting resume {resume_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the resume. Please try again."
        ) 