from typing import List, Optional
from pydantic import BaseModel

class RequiredSkill(BaseModel):
    name: str
    years: Optional[float] = None
    importance: str = "required"  # required, preferred
    weight: float = 1.0

class JobDescription(BaseModel):
    title: str
    description: str
    required_skills: List[RequiredSkill]
    preferred_skills: List[RequiredSkill] = []
    min_experience: Optional[float] = None
    education_level: Optional[str] = None

class SkillMatch(BaseModel):
    skill: str
    match_type: str  # direct, related, missing
    years: Optional[float] = None
    similarity_score: Optional[float] = None
    related_skill: Optional[str] = None

class ResumeMatch(BaseModel):
    resume_id: int
    match_percentage: float
    skill_matches: List[SkillMatch]
    missing_skills: List[RequiredSkill]
    recommendation: str  # Strong Match, Good Match, Consider, Not Recommended
    confidence_score: float
    explanation: List[str]
    improvement_suggestions: List[str]
