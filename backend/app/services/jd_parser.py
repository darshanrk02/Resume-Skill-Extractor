import re
from typing import List, Dict, Any
import spacy
from ..models.job_description import JobDescription, RequiredSkill

class JDParser:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

        # Common skill keywords
        self.tech_skills = [
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "PHP",
            "HTML", "CSS", "SQL", "NoSQL", "React", "Angular", "Vue", "Node.js",
            "Django", "Flask", "Spring", "ASP.NET", "AWS", "Azure", "Docker",
            "Kubernetes", "Git", "CI/CD", "REST API", "GraphQL", "MongoDB"
        ]

        # Education levels
        self.education_levels = [
            "Bachelor", "BS", "BA", "B.S.", "B.A.", "Master", "MS", "MA", "M.S.",
            "M.A.", "PhD", "Ph.D.", "Doctorate", "Associate", "Diploma"
        ]

    def parse(self, text: str) -> JobDescription:
        """Parse job description text into structured format"""
        # Clean and normalize text
        text = text.replace('\n', ' ').replace('\r', ' ')
        doc = self.nlp(text)

        # Extract job title
        title = self._extract_title(doc)

        # Extract required and preferred skills
        required_skills, preferred_skills = self._extract_skills(text)

        # Extract minimum experience
        min_experience = self._extract_min_experience(text)

        # Extract education level
        education_level = self._extract_education_level(text)

        return JobDescription(
            title=title,
            description=text,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            min_experience=min_experience,
            education_level=education_level
        )

    def _extract_title(self, doc) -> str:
        """Extract job title from the text"""
        # Look for job title patterns
        title_patterns = [
            r"(?i)(Senior|Junior|Lead|Principal|Staff)?\s*(Software|Frontend|Backend|Full Stack|DevOps|ML|AI)?\s*(Engineer|Developer|Architect)",
            r"(?i)(Data|Machine Learning|AI|Business Intelligence)\s*(Scientist|Engineer|Analyst)",
            r"(?i)(Product|Project|Program)\s*(Manager|Lead|Owner)"
        ]

        for sent in doc.sents:
            for pattern in title_patterns:
                match = re.search(pattern, sent.text)
                if match:
                    return match.group(0).strip()

        # If no specific pattern found, return first sentence or default
        return next(doc.sents).text.strip() if doc.sents else "Software Engineer"

    def _extract_skills(self, text: str) -> tuple[List[RequiredSkill], List[RequiredSkill]]:
        """Extract required and preferred skills from text"""
        required_skills = []
        preferred_skills = []

        # Split text into sections
        sections = {
            "required": "",
            "preferred": ""
        }

        # Look for required/preferred sections
        required_pattern = r"(?i)(required|must have|key|essential)(?:\s+skills|\s+qualifications)?:(.*?)(?=\n\n|\Z)"
        preferred_pattern = r"(?i)(preferred|nice to have|plus|desired)(?:\s+skills|\s+qualifications)?:(.*?)(?=\n\n|\Z)"

        required_match = re.search(required_pattern, text, re.DOTALL)
        if required_match:
            sections["required"] = required_match.group(2)

        preferred_match = re.search(preferred_pattern, text, re.DOTALL)
        if preferred_match:
            sections["preferred"] = preferred_match.group(2)

        # If no explicit sections found, treat all as required
        if not sections["required"] and not sections["preferred"]:
            sections["required"] = text

        # Extract skills from each section
        for skill in self.tech_skills:
            # Look for skill with years of experience
            pattern = fr"(?i){re.escape(skill)}\s*(?:\(|\[)?(\d+(?:\.\d+)?(?:\+|\s*-\s*\d+(?:\.\d+)?)?)\s*(?:years?|yrs?)?"

            # Check required section
            if re.search(fr"\b{re.escape(skill)}\b", sections["required"], re.IGNORECASE):
                years_match = re.search(pattern, sections["required"])
                years = float(years_match.group(1).replace("+", "")) if years_match else None
                required_skills.append(RequiredSkill(
                    name=skill,
                    years=years,
                    importance="required",
                    weight=1.0
                ))

            # Check preferred section
            elif re.search(fr"\b{re.escape(skill)}\b", sections["preferred"], re.IGNORECASE):
                years_match = re.search(pattern, sections["preferred"])
                years = float(years_match.group(1).replace("+", "")) if years_match else None
                preferred_skills.append(RequiredSkill(
                    name=skill,
                    years=years,
                    importance="preferred",
                    weight=0.5
                ))

        return required_skills, preferred_skills

    def _extract_min_experience(self, text: str) -> float:
        """Extract minimum years of experience required"""
        patterns = [
            r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience",
            r"(?:minimum|min\.?|at\s+least)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s+(?:of\s+)?experience\s+(?:required|needed)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        return None

    def _extract_education_level(self, text: str) -> str:
        """Extract required education level"""
        for level in self.education_levels:
            if re.search(fr"\b{re.escape(level)}\b", text, re.IGNORECASE):
                return level
        return None
