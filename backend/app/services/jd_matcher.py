from typing import List, Dict, Any
import numpy as np
from ..models.job_description import JobDescription, ResumeMatch, SkillMatch, RequiredSkill
from ..models.resume import ResumeData

class JDMatcher:
    def __init__(self):
        # Define skill relationships for better matching
        self.related_skills = {
            "python": ["django", "flask", "fastapi", "pyramid"],
            "javascript": ["typescript", "nodejs", "react", "vue", "angular"],
            "java": ["spring", "hibernate", "junit", "maven"],
            "cloud": ["aws", "azure", "gcp", "docker", "kubernetes"],
            "database": ["sql", "mysql", "postgresql", "mongodb", "redis"],
            "testing": ["junit", "pytest", "jest", "selenium", "cypress"],
            "version_control": ["git", "svn", "mercurial"],
            "ci_cd": ["jenkins", "travis", "gitlab-ci", "github-actions"]
        }

    def match_resume(self, resume_data: ResumeData, job_description: JobDescription) -> ResumeMatch:
        """Match a resume against a job description"""
        # Extract skills from resume
        resume_skills = [skill.name for skill in resume_data.skills]
        
        # Match skills
        skill_matches = []
        missing_skills = []
        total_weight = 0
        matched_weight = 0

        # Process required skills
        for req_skill in job_description.required_skills:
            total_weight += req_skill.weight
            match = self._find_skill_match(req_skill.name, resume_skills, resume_data)
            
            if match:
                skill_matches.append(match)
                if match.match_type == "direct":
                    matched_weight += req_skill.weight
                else:  # related match
                    matched_weight += req_skill.weight * match.similarity_score
            else:
                missing_skills.append(req_skill)

        # Process preferred skills
        for pref_skill in job_description.preferred_skills:
            total_weight += pref_skill.weight
            match = self._find_skill_match(pref_skill.name, resume_skills, resume_data)
            
            if match:
                skill_matches.append(match)
                if match.match_type == "direct":
                    matched_weight += pref_skill.weight
                else:  # related match
                    matched_weight += pref_skill.weight * match.similarity_score

        # Calculate match percentage
        match_percentage = (matched_weight / total_weight * 100) if total_weight > 0 else 0

        # Generate recommendation
        recommendation, confidence_score, explanation, suggestions = self._generate_recommendation(
            match_percentage,
            skill_matches,
            missing_skills,
            job_description,
            resume_data
        )

        return ResumeMatch(
            resume_id=resume_data.id,
            match_percentage=round(match_percentage, 2),
            skill_matches=skill_matches,
            missing_skills=missing_skills,
            recommendation=recommendation,
            confidence_score=round(confidence_score, 2),
            explanation=explanation,
            improvement_suggestions=suggestions
        )

    def _find_skill_match(self, required_skill: str, resume_skills: List[str], resume_data: ResumeData) -> SkillMatch:
        """Find a match for a required skill in the resume skills"""
        # Check for direct match
        for skill in resume_skills:
            if self._normalize_skill(skill) == self._normalize_skill(required_skill):
                years = self._get_skill_years(skill, resume_data)
                return SkillMatch(
                    skill=skill,
                    match_type="direct",
                    years=years,
                    similarity_score=1.0
                )

        # Check for related skills
        related_match = self._find_related_skill(required_skill, resume_skills)
        if related_match:
            years = self._get_skill_years(related_match[0], resume_data)
            return SkillMatch(
                skill=related_match[0],
                match_type="related",
                years=years,
                similarity_score=related_match[1],
                related_skill=required_skill
            )

        return None

    def _normalize_skill(self, skill: str) -> str:
        """Normalize skill name for comparison"""
        return skill.lower().strip().replace('-', '').replace(' ', '')

    def _find_related_skill(self, required_skill: str, resume_skills: List[str]) -> tuple:
        """Find a related skill match using predefined relations"""
        if not resume_skills:
            return None

        # Check predefined related skills
        req_normalized = self._normalize_skill(required_skill)
        for category, related in self.related_skills.items():
            if req_normalized in map(self._normalize_skill, related):
                for skill in resume_skills:
                    if self._normalize_skill(skill) in map(self._normalize_skill, related):
                        return (skill, 0.8)  # High similarity for predefined relations

        # Simple string matching fallback
        for skill in resume_skills:
            # Check if one contains the other
            skill_norm = self._normalize_skill(skill)
            req_norm = self._normalize_skill(required_skill)
            
            if skill_norm in req_norm or req_norm in skill_norm:
                similarity = 0.7  # Decent similarity for substring matches
                return (skill, similarity)
                
        return None

    def _get_skill_years(self, skill: str, resume_data: ResumeData) -> float:
        """Extract years of experience for a skill from resume data"""
        # Look in experience sections for skill mentions
        total_years = 0
        for exp in resume_data.experience:
            if exp.description and self._normalize_skill(skill) in self._normalize_skill(exp.description):
                # Calculate years between start and end dates
                # This is a simplified calculation
                if exp.start_date and exp.end_date:
                    try:
                        start_year = float(exp.start_date.split()[-1])
                        end_year = float(exp.end_date.split()[-1])
                        total_years += end_year - start_year
                    except (ValueError, IndexError):
                        pass
        
        return round(total_years, 1) if total_years > 0 else None

    def _generate_recommendation(
        self,
        match_percentage: float,
        skill_matches: List[SkillMatch],
        missing_skills: List[RequiredSkill],
        job_description: JobDescription,
        resume_data: ResumeData
    ) -> tuple[str, float, List[str], List[str]]:
        """Generate recommendation and explanation based on match analysis"""
        # Initialize lists for explanation and suggestions
        explanation = []
        suggestions = []
        
        # Calculate confidence score based on data completeness
        confidence_factors = [
            bool(resume_data.contact_info),
            bool(resume_data.skills),
            bool(resume_data.education),
            bool(resume_data.experience),
            len(skill_matches) > 0
        ]
        confidence_score = sum(confidence_factors) / len(confidence_factors)

        # Determine recommendation based on match percentage
        if match_percentage >= 85:
            recommendation = "Strong Match"
            explanation.append(f"Strong overall match with {match_percentage:.1f}% alignment to job requirements")
        elif match_percentage >= 70:
            recommendation = "Good Match"
            explanation.append(f"Good match with {match_percentage:.1f}% alignment to job requirements")
        elif match_percentage >= 50:
            recommendation = "Consider"
            explanation.append(f"Moderate match with {match_percentage:.1f}% alignment to job requirements")
        else:
            recommendation = "Not Recommended"
            explanation.append(f"Low match with only {match_percentage:.1f}% alignment to job requirements")

        # Add specific explanations
        direct_matches = [m for m in skill_matches if m.match_type == "direct"]
        related_matches = [m for m in skill_matches if m.match_type == "related"]
        
        if direct_matches:
            explanation.append(f"Directly matched {len(direct_matches)} skills")
        
        if related_matches:
            explanation.append(f"Found {len(related_matches)} related skills that could be leveraged")
        
        if missing_skills:
            critical_missing = [s.name for s in missing_skills if s.weight >= 8]
            if critical_missing:
                explanation.append(f"Missing critical skills: {', '.join(critical_missing)}")
                suggestions.append(f"Consider acquiring these critical skills: {', '.join(critical_missing)}")
        
        # Add improvement suggestions
        if missing_skills:
            # Group by category to make suggestions more coherent
            missing_by_category = {}
            for skill in missing_skills:
                for category, related_skills in self.related_skills.items():
                    if self._normalize_skill(skill.name) in map(self._normalize_skill, related_skills):
                        if category not in missing_by_category:
                            missing_by_category[category] = []
                        missing_by_category[category].append(skill.name)
                        break
            
            for category, skills in missing_by_category.items():
                if len(skills) > 1:
                    suggestions.append(f"Consider improving {category} skills, particularly: {', '.join(skills)}")
        
        return recommendation, confidence_score, explanation, suggestions
