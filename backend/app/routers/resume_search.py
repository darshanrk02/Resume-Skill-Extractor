# from fastapi import APIRouter, Depends, HTTPException, Query
# from typing import List, Optional
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta

# from ..models.sql_models import Resume, ContactInfo, Skill, Education, Experience, Project
# from ..database import get_db
# from ..models.resume import ResumeData

# router = APIRouter(
#     prefix="/api/v1/resumes",
#     tags=["resume_search"],
#     responses={404: {"description": "Not found"}},
# )

# @router.get("/", response_model=List[dict])
# async def search_resumes(
#     skill: Optional[str] = Query(None, description="Filter by skill"),
#     min_experience: Optional[int] = Query(None, description="Minimum years of experience"),
#     education: Optional[str] = Query(None, description="Filter by education level"),
#     db: Session = Depends(get_db)
# ):
#     """
#     Search resumes with filters
#     """
#     query = db.query(Resume)
    
#     # Apply filters if provided
#     if skill:
#         query = query.join(Skill).filter(Skill.name.ilike(f"%{skill}%"))
    
#     if education:
#         query = query.join(Education).filter(Education.degree.ilike(f"%{education}%"))
    
#     # Execute query
#     resumes = query.all()
    
#     # Format response
#     result = []
#     for resume in resumes:
#         # Get contact info
#         contact = db.query(ContactInfo).filter(ContactInfo.resume_id == resume.id).first()
#         skills = db.query(Skill).filter(Skill.resume_id == resume.id).all()
        
#         result.append({
#             "id": resume.id,
#             "filename": resume.filename,
#             "upload_date": resume.upload_date,
#             "name": contact.name if contact else "",
#             "email": contact.email if contact else "",
#             "skills": [{"name": s.name} for s in skills],
#         })
    
#     return result

# @router.get("/{resume_id}", response_model=dict)
# async def get_resume_details(
#     resume_id: int,
#     db: Session = Depends(get_db)
# ):
#     """
#     Get detailed information about a specific resume
#     """
#     resume = db.query(Resume).filter(Resume.id == resume_id).first()
#     if not resume:
#         raise HTTPException(status_code=404, detail="Resume not found")
    
#     # Get all related data
#     contact = db.query(ContactInfo).filter(ContactInfo.resume_id == resume_id).first()
#     skills = db.query(Skill).filter(Skill.resume_id == resume_id).all()
#     education = db.query(Education).filter(Education.resume_id == resume_id).all()
#     experience = db.query(Experience).filter(Experience.resume_id == resume_id).all()
#     projects = db.query(Project).filter(Project.resume_id == resume_id).all()
    
#     return {
#         "id": resume.id,
#         "filename": resume.filename,
#         "upload_date": resume.upload_date,
#         "contact": {
#             "name": contact.name if contact else None,
#             "email": contact.email if contact else None,
#             "phone": contact.phone if contact else None,
#             "location": contact.location if contact else None,
#             "linkedin": contact.linkedin if contact else None,
#             "github": contact.github if contact else None,
#             "portfolio": contact.portfolio if contact else None,
#         },
#         "skills": [{"name": s.name, "category": s.category} for s in skills],
#         "education": [{
#             "institution": e.institution,
#             "degree": e.degree,
#             "field_of_study": e.field_of_study,
#             "start_date": e.start_date,
#             "end_date": e.end_date,
#             "gpa": e.gpa
#         } for e in education],
#         "experience": [{
#             "company": exp.company,
#             "position": exp.position,
#             "start_date": exp.start_date,
#             "end_date": exp.end_date,
#             "current": exp.current,
#             "description": exp.description
#         } for exp in experience],
#         "projects": [{
#             "name": p.name,
#             "description": p.description,
#             "technologies": p.technologies.split(",") if p.technologies else [],
#             "start_date": p.start_date,
#             "end_date": p.end_date,
#             "url": p.url
#         } for p in projects]
#     } 