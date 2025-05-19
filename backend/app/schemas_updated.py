from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class ContactInfoBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

class ContactInfoCreate(ContactInfoBase):
    pass

class ContactInfo(ContactInfoBase):
    id: int
    resume_id: int
    model_config = ConfigDict(from_attributes=True)

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    resume_id: int
    model_config = ConfigDict(from_attributes=True)

class EducationBase(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None

class EducationCreate(EducationBase):
    pass

class Education(EducationBase):
    id: int
    resume_id: int
    model_config = ConfigDict(from_attributes=True)

class ExperienceBase(BaseModel):
    company: str
    position: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class ExperienceCreate(ExperienceBase):
    pass

class Experience(ExperienceBase):
    id: int
    resume_id: int
    model_config = ConfigDict(from_attributes=True)

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: Optional[str] = None
    url: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    resume_id: int
    model_config = ConfigDict(from_attributes=True)

class ResumeBase(BaseModel):
    filename: str
    upload_date: str

class ResumeCreate(ResumeBase):
    contact_info: Optional[ContactInfoCreate] = None
    skills: List[SkillCreate] = []
    education: List[EducationCreate] = []
    experience: List[ExperienceCreate] = []
    projects: List[ProjectCreate] = []

class Resume(ResumeBase):
    id: int
    contact_info: Optional[ContactInfo] = None
    skills: List[Skill] = []
    education: List[Education] = []
    experience: List[Experience] = []
    projects: List[Project] = []
    model_config = ConfigDict(from_attributes=True)
