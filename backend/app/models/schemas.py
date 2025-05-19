from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ContactInfoBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
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

    class Config:
        orm_mode = True

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True

class EducationBase(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None

class EducationCreate(EducationBase):
    pass

class Education(EducationBase):
    id: int
    resume_id: int

    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True

class ResumeBase(BaseModel):
    filename: str
    upload_date: str = Field(default_factory=lambda: datetime.now().isoformat())

class ResumeCreate(ResumeBase):
    pass

class Resume(ResumeBase):
    id: int
    contact_info: Optional[ContactInfo] = None
    skills: List[Skill] = []
    education: List[Education] = []
    experience: List[Experience] = []
    projects: List[Project] = []

    class Config:
        orm_mode = True

class ResumeExtracted(BaseModel):
    contact_info: Optional[ContactInfoBase] = None
    skills: List[SkillBase] = []
    education: List[EducationBase] = []
    experience: List[ExperienceBase] = []
    projects: List[ProjectBase] = []

class ResumeSave(BaseModel):
    filename: str
    contact_info: Optional[ContactInfoBase] = None
    skills: List[SkillBase] = []
    education: List[EducationBase] = []
    experience: List[ExperienceBase] = []
    projects: List[ProjectBase] = []
