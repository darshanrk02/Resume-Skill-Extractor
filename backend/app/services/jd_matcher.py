from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from ..models.job_description import JobDescription, ResumeMatch, SkillMatch, RequiredSkill
from ..models.resume import ResumeData

class JDMatcher:
    def __init__(self):
        # Load the sentence transformer model for semantic similarity
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
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
        resume_skills = [skill["name"] for skill in resume_data.skills]
        
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
        """Find a related skill match using semantic similarity"""
        if not resume_skills:
            return None

        # First check predefined related skills
        req_normalized = self._normalize_skill(required_skill)
        for category, related in self.related_skills.items():
            if req_normalized in map(self._normalize_skill, related):
                for skill in resume_skills:
                    if self._normalize_skill(skill) in map(self._normalize_skill, related):
                        return (skill, 0.8)  # High similarity for predefined relations

        # Use semantic similarity as fallback
        required_embedding = self.model.encode([required_skill])
        skills_embedding = self.model.encode(resume_skills)
        similarities = cosine_similarity(required_embedding, skills_embedding)[0]
        
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        if best_similarity > 0.7:  # Threshold for related skills
            return (resume_skills[best_match_idx], best_similarity)
            
        return None

    def _get_skill_years(self, skill: str, resume_data: ResumeData) -> float:
        """Extract years of experience for a skill from resume data"""
        # Look in experience sections for skill mentions
        total_years = 0
        for exp in resume_data.experience:
            if self._normalize_skill(skill) in self._normalize_skill(exp.description):
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
            explanation.append(f"Directly matches {len(direct_matches)} required skills")
        
        if related_matches:
            explanation.append(f"Has {len(related_matches)} related/transferable skills")

        # Generate improvement suggestions
        if missing_skills:
            critical_missing = [s.name for s in missing_skills if s.importance == "required"]
            if critical_missing:
                explanation.append(f"Missing {len(critical_missing)} critical skills")
                suggestions.append(f"Focus on acquiring these critical skills: {', '.join(critical_missing)}")

        # Experience-based suggestions
        if job_description.min_experience:
            total_exp = sum(self._get_skill_years(skill["name"], resume_data) or 0 
                          for skill in resume_data.skills)
            if total_exp < job_description.min_experience:
                suggestions.append(f"Gain more experience (job requires {job_description.min_experience} years)")

        # Education-based suggestions
        if job_description.education_level and not any(
            edu.degree and job_description.education_level.lower() in edu.degree.lower() 
            for edu in resume_data.education
        ):
            suggestions.append(f"Consider pursuing {job_description.education_level} degree")

        return recommendation, confidence_score, explanation, suggestions
