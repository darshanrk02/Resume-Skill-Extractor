from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
from .sql_models import Resume as DBResume, ContactInfo as DBContactInfo, Skill as DBSkill, \
    Education as DBEducation, Experience as DBExperience, Project as DBProject, Tag as DBTag

class ContactInfo(BaseModel):
    """Contact information model for a resume."""
    name: Optional[str] = Field(None, description="Full name of the candidate")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Current location")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(None, description="Personal website or portfolio URL")

    @classmethod
    def from_db_model(cls, db_contact: DBContactInfo) -> 'ContactInfo':
        """Create a ContactInfo instance from a database model."""
        return cls(
            name=db_contact.name,
            email=db_contact.email,
            phone=db_contact.phone,
            location=db_contact.location,
            linkedin=db_contact.linkedin,
            github=db_contact.github,
            portfolio=db_contact.portfolio
        )

class Skill(BaseModel):
    """Skill model."""
    name: str = Field(..., description="Skill name")
    category: Optional[str] = Field(None, description="Skill category")

class Tag(BaseModel):
    """Tag model for resume categorization."""
    id: Optional[int] = Field(None, description="Tag ID")
    name: str = Field(..., description="Tag name")
    
    @classmethod
    def from_db_model(cls, db_tag: DBTag) -> 'Tag':
        """Create a Tag instance from a database model."""
        return cls(
            id=db_tag.id,
            name=db_tag.name
        )

class Education(BaseModel):
    """Education information model."""
    institution: str = Field(..., description="Name of the educational institution")
    degree: Optional[str] = Field(None, description="Degree obtained or pursuing")
    field_of_study: Optional[str] = Field(None, description="Field of study")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM or YYYY)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM or YYYY), or None if current")
    gpa: Optional[str] = Field(None, description="GPA or grade")
    description: Optional[str] = Field(None, description="Additional details about the education")

    @classmethod
    def from_db_model(cls, db_edu: DBEducation) -> 'Education':
        """Create an Education instance from a database model."""
        return cls(
            institution=db_edu.institution,
            degree=db_edu.degree,
            field_of_study=db_edu.field_of_study,
            start_date=db_edu.start_date,
            end_date=db_edu.end_date,
            gpa=db_edu.gpa,
            description=db_edu.description
        )

class Experience(BaseModel):
    """Work experience model."""
    company: str = Field(..., description="Name of the company")
    position: str = Field(..., description="Job title/position")
    location: Optional[str] = Field(None, description="Location of employment")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM or YYYY)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM or YYYY), or None if current")
    current: bool = Field(False, description="Whether this is the current position")
    description: Optional[str] = Field(None, description="Job description and responsibilities")
    skills: List[str] = Field(default_factory=list, description="List of skills used in this role")

    @classmethod
    def from_db_model(cls, db_exp: DBExperience) -> 'Experience':
        """Create an Experience instance from a database model."""
        return cls(
            company=db_exp.company,
            position=db_exp.position,
            location=db_exp.location,
            start_date=db_exp.start_date,
            end_date=db_exp.end_date,
            current=db_exp.current,
            description=db_exp.description,
            skills=[]  # Skills would need to be loaded separately
        )

class Project(BaseModel):
    """Project information model."""
    name: str = Field(..., description="Name of the project")
    description: str = Field(..., description="Description of the project")
    technologies: List[str] = Field(default_factory=list, description="Technologies used")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM or YYYY)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM or YYYY), or None if ongoing")
    url: Optional[str] = Field(None, description="Project URL or repository link")

    @classmethod
    def from_db_model(cls, db_proj: DBProject) -> 'Project':
        """Create a Project instance from a database model."""
        return cls(
            name=db_proj.name,
            description=db_proj.description or "",
            technologies=db_proj.technologies.split(",") if db_proj.technologies else [],
            start_date=db_proj.start_date,
            end_date=db_proj.end_date,
            url=db_proj.url
        )

class ResumeData(BaseModel):
    """Main resume data model that combines all sections."""
    contact_info: ContactInfo = Field(..., description="Contact information")
    summary: Optional[str] = Field(None, description="Professional summary or objective")
    skills: List[Skill] = Field(default_factory=list, description="List of skills")
    experience: List[Experience] = Field(default_factory=list, description="Work experience")
    education: List[Education] = Field(default_factory=list, description="Education history")
    projects: List[Project] = Field(default_factory=list, description="Projects")
    certifications: List[str] = Field(default_factory=list, description="Certifications")
    languages: List[Dict[str, str]] = Field(default_factory=list, description="Languages and proficiency levels")
    raw_text: Optional[str] = Field(None, description="Raw text content of the resume")
    file_name: Optional[str] = Field(None, description="Original filename")
    file_type: Optional[str] = Field(None, description="File type (e.g., pdf, docx)")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    tags: List[Tag] = Field(default_factory=list, description="Tags for categorizing resumes")

    @classmethod
    def from_db_model(cls, db_resume: DBResume) -> 'ResumeData':
        """Create a ResumeData instance from a database model."""
        return cls(
            contact_info=ContactInfo.from_db_model(db_resume.contact_info) if db_resume.contact_info else ContactInfo(),
            skills=[Skill(name=skill.name, category=skill.category) for skill in db_resume.skills],
            education=[Education.from_db_model(edu) for edu in db_resume.education],
            experience=[Experience.from_db_model(exp) for exp in db_resume.experience],
            projects=[Project.from_db_model(proj) for proj in db_resume.projects],
            tags=[Tag.from_db_model(tag) for tag in db_resume.tags],
            file_name=db_resume.filename,
            created_at=db_resume.upload_date,
            updated_at=db_resume.upload_date
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return self.dict(exclude_none=True)

    def get_skills_with_categories(self) -> Dict[str, List[str]]:
        """Organize skills by category."""
        # This is a simplified version - you might want to implement more sophisticated categorization
        categories = {
            'languages': [],
            'frameworks': [],
            'tools': [],
            'databases': [],
            'cloud': [],
            'other': []
        }
        
        for skill in self.skills:
            skill_name = skill.name.lower()
            if any(term in skill_name for term in ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby']):
                categories['languages'].append(skill.name)
            elif any(term in skill_name for term in ['react', 'angular', 'vue', 'django', 'flask', 'spring', '.net']):
                categories['frameworks'].append(skill.name)
            elif any(term in skill_name for term in ['git', 'docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'gcp']):
                categories['tools'].append(skill.name)
            elif any(term in skill_name for term in ['sql', 'mysql', 'postgresql', 'mongodb', 'redis']):
                categories['databases'].append(skill.name)
            elif any(term in skill_name for term in ['aws', 'azure', 'gcp', 'cloud']):
                categories['cloud'].append(skill.name)
            else:
                categories['other'].append(skill.name)
                
        return {k: v for k, v in categories.items() if v}  # Remove empty categories
