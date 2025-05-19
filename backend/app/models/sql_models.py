from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    upload_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    contact_info: Mapped[Optional["ContactInfo"]] = relationship(
        "ContactInfo", back_populates="resume", uselist=False, cascade="all, delete-orphan"
    )
    skills: Mapped[List["Skill"]] = relationship(
        "Skill", back_populates="resume", cascade="all, delete-orphan"
    )
    education: Mapped[List["Education"]] = relationship(
        "Education", back_populates="resume", cascade="all, delete-orphan"
    )
    experience: Mapped[List["Experience"]] = relationship(
        "Experience", back_populates="resume", cascade="all, delete-orphan"
    )
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="resume", cascade="all, delete-orphan"
    )

class ContactInfo(Base):
    __tablename__ = "contact_info"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    location: Mapped[Optional[str]] = mapped_column(String(255))
    linkedin: Mapped[Optional[str]] = mapped_column(String(255))
    github: Mapped[Optional[str]] = mapped_column(String(255))
    portfolio: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Relationship
    resume: Mapped["Resume"] = relationship("Resume", back_populates="contact_info")

class Skill(Base):
    __tablename__ = "skills"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"))
    name: Mapped[str] = mapped_column(String(255))
    category: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Relationship
    resume: Mapped["Resume"] = relationship("Resume", back_populates="skills")

class Education(Base):
    __tablename__ = "education"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"))
    institution: Mapped[str] = mapped_column(String(255))
    degree: Mapped[Optional[str]] = mapped_column(String(255))
    field_of_study: Mapped[Optional[str]] = mapped_column(String(255))
    start_date: Mapped[Optional[str]] = mapped_column(String(50))
    end_date: Mapped[Optional[str]] = mapped_column(String(50))
    gpa: Mapped[Optional[str]] = mapped_column(String(20))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationship
    resume: Mapped["Resume"] = relationship("Resume", back_populates="education")

class Experience(Base):
    __tablename__ = "experience"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"))
    company: Mapped[str] = mapped_column(String(255))
    position: Mapped[str] = mapped_column(String(255))
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    start_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    end_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    current: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationship
    resume: Mapped["Resume"] = relationship("Resume", back_populates="experience")

class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    technologies: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    start_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    end_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Relationship
    resume: Mapped["Resume"] = relationship("Resume", back_populates="projects")
