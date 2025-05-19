from typing import List, Optional, Dict, Any, Set
import os
import uuid
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import tempfile

from app.models.database import get_db
from app.models.job_description import JobDescription, ResumeMatch, SkillMatch, RequiredSkill
from app.models.resume import ResumeData
from app.services.jd_parser import JDParser
from app.services.jd_matcher import JDMatcher
from app.services.resume_parser import parse_uploaded_resume, parse_resume
from app.crud import get_resume_by_id, get_all_resumes, create_resume
from app.config import settings

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
jd_parser = JDParser()
jd_matcher = JDMatcher()

# Ensure upload directory exists
UPLOAD_DIR = settings.UPLOAD_DIR or os.path.join(tempfile.gettempdir(), 'resume_uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper methods for analysis
def categorize_skill(skill: str) -> str:
    """Categorize a skill into a general category."""
    skill = skill.lower()
    categories = {
        'languages': {'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'typescript'},
        'frontend': {'react', 'angular', 'vue', 'html', 'css', 'sass', 'bootstrap', 'tailwind', 'redux'},
        'backend': {'node.js', 'express', 'django', 'flask', 'spring', 'laravel', 'ruby on rails', 'asp.net'},
        'database': {'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'dynamodb'},
        'devops': {'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'google cloud', 'ci/cd', 'jenkins', 'github actions'},
        'tools': {'git', 'github', 'gitlab', 'jira', 'confluence', 'docker', 'kubernetes', 'ansible', 'terraform'},
        'ai_ml': {'machine learning', 'deep learning', 'ai', 'data science', 'nlp', 'computer vision', 'tensorflow', 'pytorch'},
        'mobile': {'react native', 'flutter', 'ios', 'android', 'swift', 'kotlin'},
        'testing': {'jest', 'mocha', 'pytest', 'junit', 'selenium', 'cypress'},
        'cloud': {'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean'},
        'methodologies': {'agile', 'scrum', 'kanban', 'lean', 'devops', 'ci/cd'}
    }
    
    for category, skills in categories.items():
        if skill in skills:
            return category
    return 'other'

def calculate_skill_weight(skill: str, job_description: Any) -> float:
    """Calculate weight for a skill based on job description requirements."""
    try:
        # Check if skill is in required skills
        required_skills = getattr(job_description, 'required_skills', [])
        for req_skill in required_skills:
            skill_name = getattr(req_skill, 'name', '').lower()
            if skill_name and skill_name.lower() == skill.lower():
                return getattr(req_skill, 'weight', 1.0) * 2  # Higher weight for required skills
        
        # Check if skill is in preferred skills
        preferred_skills = getattr(job_description, 'preferred_skills', [])
        for pref_skill in preferred_skills:
            skill_name = getattr(pref_skill, 'name', '').lower()
            if skill_name and skill_name.lower() == skill.lower():
                return getattr(pref_skill, 'weight', 1.0) * 1.5  # Medium weight for preferred skills
        
        return 1.0  # Default weight
    except Exception as e:
        logger.error(f"Error calculating skill weight: {str(e)}", exc_info=True)
        return 1.0  # Fallback to default weight

def generate_recommendation(
    match_percentage: float,
    matched_skills_count: int,
    total_required_skills: int
) -> str:
    """Generate a recommendation based on the match percentage."""
    if match_percentage >= 0.8:
        return "Excellent Match! Your skills align very well with the job requirements."
    elif match_percentage >= 0.6:
        return "Good Match. You have many of the required skills but could improve in some areas."
    elif match_percentage >= 0.4:
        return "Moderate Match. Consider gaining more experience with the required skills."
    else:
        return "Needs Improvement. The job requires skills that are not currently on your resume."

def generate_analysis(
    match_percentage: float,
    matched_skills_count: int,
    total_required_skills: int,
    missing_skills_count: int
) -> List[str]:
    """Generate a detailed analysis of the resume match."""
    analysis = []
    
    # Add match percentage
    analysis.append(
        f"Your resume matches {match_percentage:.1%} of the required skills "
        f"({matched_skills_count} out of {total_required_skills})."
    )
    
    # Add match level
    if match_percentage >= 0.8:
        analysis.append("This is an excellent match for the position!")
    elif match_percentage >= 0.6:
        analysis.append("This is a good match, but there's room for improvement.")
    elif match_percentage >= 0.4:
        analysis.append("This is a moderate match. Consider adding more relevant skills.")
    else:
        analysis.append("The match is below average. Consider gaining more relevant experience.")
    
    # Add missing skills info
    if missing_skills_count > 0:
        analysis.append(
            f"You're missing {missing_skills_count} key skills that are required for this position."
        )
    
    # Add recommendations
    if match_percentage < 0.8:
        if missing_skills_count > 0:
            analysis.append("Consider adding the missing skills to your resume.")
        analysis.append("Highlight your most relevant experience and projects.")
    
    return analysis

@router.post("/analyze", response_model=Dict[str, Any], tags=["jd_matching"])
async def analyze_resume_jd_match(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: Optional[str] = Form(None),
    company: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Analyze a resume against a job description.
    
    This endpoint accepts a resume file and job description text, then performs
    analysis to determine how well the resume matches the job requirements.
    """
    try:
        logger.info(f"Starting resume analysis for file: {resume.filename}")
        
        # Parse the resume
        try:
            resume_data = await parse_uploaded_resume(resume)
            logger.debug(f"Resume data parsed successfully")
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}", exc_info=True)
            raise HTTPException(status_code=400, detail=f"Error parsing resume: {str(e)}")
            
        
        # Parse the job description
        try:
            logger.debug(f"Parsing job description: {job_description[:200]}...")  # Log first 200 chars
            parsed_jd = jd_parser.parse(job_description)
            logger.debug(f"Parsed JD: {parsed_jd}")
        except Exception as e:
            logger.error(f"Error parsing job description: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=400, 
                detail=f"Error parsing job description: {str(e)}"
            )
        
        # Extract skills from resume
        from ..utils.text_utils import extract_skills
        
        try:
            # Get skills from resume data if available, otherwise extract from text
            if hasattr(resume_data, 'skills') and resume_data.skills:
                resume_skills = set(skill.name.lower() for skill in resume_data.skills)
                logger.debug(f"Using resume_data.skills: {resume_skills}")
            else:
                resume_text = getattr(resume_data, 'summary', '') or getattr(resume_data, 'description', '')
                logger.debug(f"Extracting skills from resume text: {resume_text[:200]}...")
                extracted_skills = extract_skills(resume_text)
                resume_skills = set(skill.name.lower() for skill in extracted_skills)
                
            if not resume_skills:
                logger.warning("No skills found in resume")
                
        except Exception as e:
            logger.error(f"Error extracting skills from resume: {str(e)}", exc_info=True)
            resume_skills = set()  # Continue with empty skills if there's an error
        
        logger.debug(f"Resume skills: {resume_skills}")
        
        # Get the job description text and extract skills
        try:
            jd_text = getattr(parsed_jd, 'description', '')
            logger.debug(f"Extracting skills from job description: {jd_text[:200]}...")
            extracted_jd_skills = extract_skills(jd_text)
            jd_skills = set(skill.name.lower() for skill in extracted_jd_skills)
            logger.debug(f"Extracted job description skills: {jd_skills}")
            
            if not jd_skills:
                logger.warning("No skills found in job description")
                
        except Exception as e:
            logger.error(f"Error extracting skills from job description: {str(e)}", exc_info=True)
            jd_skills = set()
        
        # Calculate matches and missing skills
        try:
            matched_skills = resume_skills.intersection(jd_skills)
            missing_skills = jd_skills - resume_skills
        except Exception as e:
            logger.error(f"Error calculating skill matches: {str(e)}", exc_info=True)
            matched_skills = set()
            missing_skills = set()
        
        # Calculate match metrics
        total_required_skills = len(jd_skills)
        matched_skills_count = len(matched_skills)
        
        # Avoid division by zero
        match_percentage = (
            (matched_skills_count / total_required_skills) 
            if total_required_skills > 0 else 0.0
        )
        
        # Generate detailed response
        try:
            # Convert sets to lists for JSON serialization
            matched_skills_list = [
                {
                    "skill": skill,
                    "category": categorize_skill(skill),
                    "weight": calculate_skill_weight(skill, parsed_jd)
                }
                for skill in sorted(matched_skills)  # Sort for consistent ordering
            ]
            
            # Get job title and company from the parsed JD or use defaults
            job_title_value = job_title or getattr(parsed_jd, 'title', 'Not specified')
            company_value = company or getattr(parsed_jd, 'company', 'Not specified')
            
            # Generate the response
            response = {
                "resume_id": 1,  # In a real app, this would be the database ID
                "match_percentage": float(match_percentage),  # Ensure it's JSON serializable
                "resume_skills": sorted(list(resume_skills)),
                "job_skills": sorted(list(jd_skills)),
                "skill_matches": [
                    {
                        "skill": skill, 
                        "similarity_score": 1.0,
                        "category": categorize_skill(skill)
                    }
                    for skill in sorted(matched_skills)
                ],
                "missing_skills": [
                    {
                        "name": skill, 
                        "weight": calculate_skill_weight(skill, parsed_jd),
                        "category": categorize_skill(skill)
                    }
                    for skill in sorted(missing_skills)
                ],
                "recommendation": generate_recommendation(
                    match_percentage, 
                    matched_skills_count,
                    total_required_skills
                ),
                "confidence_score": min(1.0, match_percentage * 1.2),  # Cap at 1.0
                "analysis": generate_analysis(
                    match_percentage,
                    matched_skills_count,
                    total_required_skills,
                    len(missing_skills)
                ),
                "metadata": {
                    "resume_file_name": resume.filename,
                    "resume_file_type": resume.content_type,
                    "job_title": job_title_value,
                    "company": company_value,
                    "processed_at": datetime.utcnow().isoformat()
                }
            }
            
            logger.debug(f"Generated response: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Error generating response: {str(e)}"
            )
    except HTTPException:
        raise
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        import traceback
        error_msg = f"Error in analyze_resume_jd_match: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to process resume and job description",
                "details": str(e)
            }
        )

@router.post("/api/v1/parse-job-description")
async def parse_job_description(text: str = Form(...)):
    """
    Parse raw job description text into structured format
    """
    try:
        parsed_jd = jd_parser.parse(text)
        return parsed_jd
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing job description: {str(e)}")

# Keep the old endpoints for backward compatibility
@router.post("/jd/analyze", response_model=List[ResumeMatch], deprecated=True)
async def analyze_job_description(
    job_description: JobDescription,
    resume_id: int = None,
    db: Session = Depends(get_db)
):
    """
    [Deprecated] Use /api/v1/analyze instead.
    Analyze a job description against one or all stored resumes.
    """
    try:
        # Parse the job description
        parsed_jd = job_description
        
        # Get resume(s) to match against
        if resume_id is not None:
            resume = get_resume_by_id(db, resume_id)
            if not resume:
                raise HTTPException(status_code=404, detail="Resume not found")
            resumes = [resume]
        else:
            resumes = get_all_resumes(db)
            if not resumes:
                raise HTTPException(status_code=404, detail="No resumes found in database")

        # Match against each resume
        matches = []
        for resume in resumes:
            match_result = jd_matcher.match_resume(resume, parsed_jd)
            matches.append(match_result)

        # Sort matches by match percentage in descending order
        matches.sort(key=lambda x: x.match_percentage, reverse=True)
        
        return matches

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing job description: {str(e)}")
