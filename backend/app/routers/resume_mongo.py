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
    Query,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse

from app.models.mongodb import get_resume_collection, get_tag_collection
from app.models.resume import ResumeData, Tag
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
        
        # Process tags if they exist
        if resume_dict.get("tags"):
            tag_collection = get_tag_collection()
            processed_tags = []
            
            for tag_data in resume_dict["tags"]:
                # Check if tag already exists
                existing_tag = tag_collection.find_one({"name": tag_data["name"]})
                if existing_tag:
                    processed_tags.append({
                        "id": str(existing_tag["_id"]),
                        "name": existing_tag["name"]
                    })
                else:
                    # Create new tag
                    new_tag_result = tag_collection.insert_one({"name": tag_data["name"]})
                    processed_tags.append({
                        "id": str(new_tag_result.inserted_id),
                        "name": tag_data["name"]
                    })
            
            # Update resume dict with processed tags
            resume_dict["tags"] = processed_tags
        
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
async def get_all_resumes(
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    skill: Optional[str] = Query(None, description="Filter by skill name")
) -> List[ResumeData]:
    """
    Get all resumes with optional tag and skill filtering
    """
    try:
        # Log the request parameters
        logger.info(f"Fetching resumes with tags: {tags}, skill: {skill}")
        
        # Get the resume collection
        resumes_collection = get_resume_collection()
        
        # Build query filter
        query_filter = {}
        
        # Add tag filter if provided
        if tags and len(tags) > 0:
            logger.info(f"Filtering by tags: {tags}")
            
            # Create a query that matches either tags OR skills with the tag name
            tag_queries = []
            
            for tag in tags:
                # Match by tags - case insensitive
                tag_queries.append({"tags.name": {"$regex": f"^{tag}$", "$options": "i"}})
                
                # Match by skills - case insensitive
                tag_queries.append({"skills.name": {"$regex": f"^{tag}$", "$options": "i"}})
            
            # Combine with OR
            query_filter["$or"] = tag_queries
            
            logger.info(f"Using case-insensitive tag/skill filter: {query_filter}")
        
        # Add skill filter if provided
        if skill:
            logger.info(f"Filtering by skill: {skill}")
            query_filter["skills.name"] = {"$regex": skill, "$options": "i"}
        
        logger.info(f"MongoDB query filter: {query_filter}")
        
        # Query all resumes, sorted by creation date
        resumes = list(resumes_collection.find(query_filter).sort("created_at", -1))
        logger.info(f"Found {len(resumes)} matching resumes")
        
        # Convert MongoDB documents to ResumeData list
        resume_list = []
        for resume in resumes:
            # Convert ObjectId to string
            resume_id = str(resume.pop("_id"))
            
            # Handle dates (convert to ISO strings)
            for date_field in ["created_at", "updated_at"]:
                if date_field in resume and isinstance(resume[date_field], datetime):
                    resume[date_field] = resume[date_field].isoformat()
            
            # Convert to Pydantic model
            resume_data = ResumeData(**resume)
            resume_list.append(resume_data)
        
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

@router.post("/resumes/{resume_id}/tags", response_model=ResumeData)
async def add_tags_to_resume(
    resume_id: str,
    tags: List[str]
) -> ResumeData:
    """
    Add tags to a resume.
    
    Args:
        resume_id: ID of the resume
        tags: List of tag names to add
        
    Returns:
        Updated resume data
    """
    try:
        # Get collections
        resumes_collection = get_resume_collection()
        tag_collection = get_tag_collection()
        
        # Convert string ID to ObjectId
        object_id = ObjectId(resume_id)
        
        # Check if resume exists
        resume = resumes_collection.find_one({"_id": object_id})
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Process each tag
        tag_objects = []
        for tag_name in tags:
            # Check if tag already exists
            existing_tag = tag_collection.find_one({"name": tag_name})
            if existing_tag:
                tag_id = str(existing_tag["_id"])
            else:
                # Create new tag
                new_tag_result = tag_collection.insert_one({"name": tag_name})
                tag_id = str(new_tag_result.inserted_id)
            
            # Create tag object
            tag_objects.append({"id": tag_id, "name": tag_name})
        
        # Update resume with new tags
        existing_tags = resume.get("tags", [])
        
        # Add new tags if they don't already exist
        for new_tag in tag_objects:
            if not any(et.get("name") == new_tag["name"] for et in existing_tags):
                existing_tags.append(new_tag)
        
        # Update resume
        resumes_collection.update_one(
            {"_id": object_id},
            {"$set": {"tags": existing_tags, "updated_at": datetime.utcnow()}}
        )
        
        # Get updated resume
        updated_resume = resumes_collection.find_one({"_id": object_id})
        
        # Convert to Pydantic model
        updated_resume.pop("_id")
        for date_field in ["created_at", "updated_at"]:
            if date_field in updated_resume and isinstance(updated_resume[date_field], datetime):
                updated_resume[date_field] = updated_resume[date_field].isoformat()
        
        return ResumeData(**updated_resume)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding tags to resume: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while adding tags: {str(e)}"
        )

@router.delete("/resumes/{resume_id}/tags/{tag_name}", response_model=ResumeData)
async def remove_tag_from_resume(
    resume_id: str,
    tag_name: str
) -> ResumeData:
    """
    Remove a tag from a resume.
    
    Args:
        resume_id: ID of the resume
        tag_name: Name of the tag to remove
        
    Returns:
        Updated resume data
    """
    try:
        # Get resume collection
        resumes_collection = get_resume_collection()
        
        # Convert string ID to ObjectId
        object_id = ObjectId(resume_id)
        
        # Check if resume exists
        resume = resumes_collection.find_one({"_id": object_id})
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Filter out the tag to remove
        existing_tags = resume.get("tags", [])
        updated_tags = [tag for tag in existing_tags if tag.get("name") != tag_name]
        
        # Update resume
        resumes_collection.update_one(
            {"_id": object_id},
            {"$set": {"tags": updated_tags, "updated_at": datetime.utcnow()}}
        )
        
        # Get updated resume
        updated_resume = resumes_collection.find_one({"_id": object_id})
        
        # Convert to Pydantic model
        updated_resume.pop("_id")
        for date_field in ["created_at", "updated_at"]:
            if date_field in updated_resume and isinstance(updated_resume[date_field], datetime):
                updated_resume[date_field] = updated_resume[date_field].isoformat()
        
        return ResumeData(**updated_resume)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing tag from resume: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while removing tag: {str(e)}"
        )

@router.get("/tags", response_model=List[Tag])
async def get_all_tags() -> List[Tag]:
    """
    Get all available tags.
    
    Returns:
        List of all tags in the system
    """
    try:
        # Get tag collection
        tag_collection = get_tag_collection()
        
        # Get all tags
        tags = list(tag_collection.find())
        
        # Convert to Pydantic models
        tag_list = []
        for tag in tags:
            tag_list.append(Tag(
                id=str(tag["_id"]),
                name=tag["name"]
            ))
        
        return tag_list
    
    except Exception as e:
        logger.error(f"Error retrieving tags: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving tags: {str(e)}"
        )

@router.get("/test/add-sample-resume", response_model=ResumeData)
async def add_sample_resume(skill_type: str = "python") -> ResumeData:
    """
    Creates a sample resume with specified skills for testing purposes
    
    Args:
        skill_type: Type of skills to include: 'python', 'javascript', or 'java'
    """
    try:
        # Get the resume collection
        resumes_collection = get_resume_collection()
        
        # Define different skill sets
        skill_sets = {
            "python": {
                "name": "Python Developer",
                "skills": [
                    {"name": "Python"},
                    {"name": "Django"},
                    {"name": "Flask"},
                    {"name": "MongoDB"},
                    {"name": "AWS"}
                ],
                "tags": [
                    {"id": "python-tag", "name": "python"},
                    {"id": "backend-tag", "name": "backend"}
                ]
            },
            "javascript": {
                "name": "JavaScript Developer",
                "skills": [
                    {"name": "JavaScript"},
                    {"name": "React"},
                    {"name": "Node.js"},
                    {"name": "HTML"},
                    {"name": "CSS"}
                ],
                "tags": [
                    {"id": "js-tag", "name": "javascript"},
                    {"id": "frontend-tag", "name": "frontend"}
                ]
            },
            "java": {
                "name": "Java Developer",
                "skills": [
                    {"name": "Java"},
                    {"name": "Spring"},
                    {"name": "SQL"},
                    {"name": "Microservices"},
                    {"name": "Docker"}
                ],
                "tags": [
                    {"id": "java-tag", "name": "java"},
                    {"id": "backend-tag", "name": "backend"}
                ]
            }
        }
        
        # Use default if specified type not found
        if skill_type not in skill_sets:
            skill_type = "python"
            
        skill_data = skill_sets[skill_type]
        
        # Create a sample resume
        sample_resume = {
            "contact_info": {
                "name": skill_data["name"],
                "email": f"{skill_type}@example.com",
                "phone": "123-456-7890",
                "location": "Test City, TS"
            },
            "summary": f"Experienced {skill_data['name']} with skills in various technologies.",
            "skills": skill_data["skills"],
            "experience": [
                {
                    "company": "Test Company",
                    "position": skill_data["name"],
                    "start_date": "2020-01",
                    "end_date": "2023-05",
                    "description": f"Developed applications using {skill_data['skills'][0]['name']}."
                }
            ],
            "education": [
                {
                    "institution": "Test University",
                    "degree": "B.S.",
                    "field_of_study": "Computer Science",
                    "start_date": "2016",
                    "end_date": "2020"
                }
            ],
            "file_name": f"{skill_type}_resume.pdf",
            "file_type": "pdf",
            "file_size": 12345,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "tags": skill_data["tags"]
        }
        
        # Insert the sample resume
        result = resumes_collection.insert_one(sample_resume)
        logger.info(f"Created sample resume with ID: {result.inserted_id}")
        
        # Get the inserted resume
        inserted_resume = resumes_collection.find_one({"_id": result.inserted_id})
        
        # Convert ObjectId to string
        resume_id = str(inserted_resume.pop("_id"))
        
        # Handle dates
        for date_field in ["created_at", "updated_at"]:
            if date_field in inserted_resume and isinstance(inserted_resume[date_field], datetime):
                inserted_resume[date_field] = inserted_resume[date_field].isoformat()
        
        # Return the resume data
        return ResumeData(**inserted_resume)
        
    except Exception as e:
        logger.error(f"Error creating sample resume: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating sample resume: {str(e)}"
        )

@router.get("/test/list-all-resumes")
async def debug_list_all_resumes():
    """
    Debug endpoint to list all resumes in the database with their skills and tags
    """
    try:
        # Get the resume collection
        resumes_collection = get_resume_collection()
        
        # Get all resumes
        resumes = list(resumes_collection.find({}))
        
        # Create a simplified list for debugging
        resume_list = []
        for resume in resumes:
            resume_list.append({
                "id": str(resume["_id"]),
                "name": resume.get("contact_info", {}).get("name", "No Name"),
                "skills": [skill.get("name") for skill in resume.get("skills", [])],
                "tags": [tag.get("name") for tag in resume.get("tags", [])]
            })
        
        logger.info(f"Found {len(resume_list)} resumes in database")
        return resume_list
        
    except Exception as e:
        logger.error(f"Error listing resumes: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing resumes: {str(e)}"
        ) 