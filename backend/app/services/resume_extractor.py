import PyPDF2
import pdfplumber
import re
import spacy
import os
from typing import Dict, List, Any, Optional
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

class ResumeExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.text = self._extract_text()
        self.sections = self._split_into_sections()
        
    def _extract_text(self) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(self.file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            if len(text.strip()) < 100:
                text = ""
                with pdfplumber.open(self.file_path) as pdf:
                    for page in pdf.pages:
                        text += (page.extract_text() or "") + "\n"
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            text = ""
        return text
    
    def _split_into_sections(self) -> Dict[str, str]:
        """Split resume text into sections based on common headers"""
        sections = {}
        section_headers = [
            "CONTACT", "PERSONAL INFO", "PROFILE", "SUMMARY", "OBJECTIVE", 
            "EDUCATION", "ACADEMIC", "QUALIFICATION",
            "EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT", "PROFESSIONAL EXPERIENCE",
            "SKILLS", "TECHNICAL SKILLS", "EXPERTISE", "COMPETENCIES",
            "PROJECTS", "PERSONAL PROJECTS", "ACADEMIC PROJECTS",
            "CERTIFICATIONS", "CERTIFICATES", "AWARDS", "ACHIEVEMENTS",
            "LANGUAGES", "INTERESTS", "HOBBIES", "ACTIVITIES",
            "PUBLICATIONS", "REFERENCES"
        ]
        pattern = r"(?i)^(?:{})[:\s]*$".format("|".join(section_headers))
        lines = self.text.split('\n')
        current_section = "HEADER"
        sections[current_section] = ""
        for line in lines:
            line = line.strip()
            if re.match(pattern, line, re.IGNORECASE):
                current_section = line.strip().upper()
                sections[current_section] = ""
            else:
                if line:
                    sections[current_section] += line + "\n"
        return sections
    
    def extract_contact_info(self) -> Dict[str, str]:
        """Extract contact information from the resume"""
        contact_info = {
            "name": "", "email": "", "phone": "", "location": "",
            "linkedin": "", "github": "", "portfolio": ""
        }
        header_text = self.sections.get("HEADER", "")
        if header_text:
            lines = header_text.strip().split('\n')
            for line in lines:
                if len(line.split()) > 1:
                    contact_info["name"] = line.strip()
                    break
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.findall(email_pattern, self.text)
        if email_matches:
            contact_info["email"] = email_matches[0]
        phone_pattern = r'(?:\+\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
        phone_matches = re.findall(phone_pattern, self.text)
        if phone_matches:
            contact_info["phone"] = phone_matches[0]
        doc = nlp(self.text[:1000])
        locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        if locations:
            contact_info["location"] = locations[0]
        linkedin_pattern = r'(?:linkedin\.com/in/|linkedin\.com/profile/view\?id=)([A-Za-z0-9_-]+)'
        linkedin_matches = re.findall(linkedin_pattern, self.text, re.IGNORECASE)
        if linkedin_matches:
            contact_info["linkedin"] = f"linkedin.com/in/{linkedin_matches[0]}"
        github_pattern = r'(?:github\.com/)([A-Za-z0-9_-]+)'
        github_matches = re.findall(github_pattern, self.text, re.IGNORECASE)
        if github_matches:
            contact_info["github"] = f"github.com/{github_matches[0]}"
        url_pattern = r'https?://(?:www\.)?([A-Za-z0-9.-]+\.[A-Za-z]{2,})(?:/\S*)?'
        url_matches = re.findall(url_pattern, self.text)
        for url in url_matches:
            if "linkedin" not in url.lower() and "github" not in url.lower():
                contact_info["portfolio"] = url
                break
        return contact_info
    
    def extract_skills(self) -> List[Dict[str, str]]:
        """Extract skills from the 'SKILLS' section"""
        skills = []
        skills_text = ""
        for section_name, content in self.sections.items():
            if "SKILLS" in section_name:
                skills_text = content
                break
        if not skills_text:
            return skills
        lines = skills_text.split('\n')
        for line in lines:
            line = line.strip()
            if ':' in line:
                category, skills_str = line.split(':', 1)
                category = category.strip()
                skills_list = [s.strip() for s in skills_str.split(',')]
                for skill in skills_list:
                    if skill:
                        skills.append({"name": skill, "category": category})
        return skills
    
    def extract_education(self) -> List[Dict[str, str]]:
        """Extract education information from the resume"""
        education_list = []
        education_text = ""
        for section_name, content in self.sections.items():
            if "EDUCATION" in section_name or "ACADEMIC" in section_name or "QUALIFICATION" in section_name:
                education_text = content
                break
        if not education_text:
            return education_list
        lines = [line.strip() for line in education_text.split('\n') if line.strip()]
        i = 0
        while i < len(lines):
            education_entry = {
                "institution": "", "degree": "", "field_of_study": "",
                "start_date": "", "end_date": "", "gpa": ""
            }
            institution_line = lines[i]
            date_pattern = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)?\s*\d{4}\s*(?:-|–|to)\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)?\s*\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)?\s*\d{4}\s*(?:-|–|to)\s*(?:Present|Current|Now)|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)?\s*\d{4}'
            date_match = re.search(date_pattern, institution_line)
            if date_match:
                date_str = date_match.group(0)
                education_entry["institution"] = institution_line.replace(date_str, '').strip()
                date_parts = re.split(r'(?:-|–|to)', date_str)
                if len(date_parts) > 1:
                    education_entry["start_date"] = date_parts[0].strip()
                    education_entry["end_date"] = date_parts[1].strip()
                else:
                    education_entry["end_date"] = date_parts[0].strip()
            else:
                education_entry["institution"] = institution_line.strip()
            i += 1
            if i < len(lines):
                degree_line = lines[i]
                degree_patterns = [
                    r'(?:Bachelor|BS|BA|B\.S\.|B\.A\.|B\.E\.|B\.Tech\.|Bachelor of Science|Bachelor of Arts|Bachelor of Engineering|Bachelor of Technology)',
                    r'(?:Master|MS|MA|M\.S\.|M\.A\.|M\.E\.|M\.Tech\.|Master of Science|Master of Arts|Master of Engineering|Master of Technology)',
                    r'(?:PhD|Ph\.D\.|Doctor of Philosophy)',
                    r'(?:Diploma|Certificate|Associate)'
                ]
                for pattern in degree_patterns:
                    degree_match = re.search(pattern, degree_line, re.IGNORECASE)
                    if degree_match:
                        education_entry["degree"] = degree_match.group(0)
                        field_pattern = r'in\s+([A-Za-z\s]+)'
                        field_match = re.search(field_pattern, degree_line)
                        if field_match:
                            education_entry["field_of_study"] = field_match.group(1).strip()
                        break
                gpa_pattern = r'(?:GPA|Grade Point Average|G\.P\.A\.)[:\s]*([0-4]\.[0-9]+)(?:/[0-9]\.[0-9]+)?'
                gpa_match = re.search(gpa_pattern, degree_line, re.IGNORECASE)
                if gpa_match:
                    education_entry["gpa"] = gpa_match.group(1)
                i += 1
            education_list.append(education_entry)
        return education_list
    
    def extract_experience(self) -> List[Dict[str, str]]:
        """Extract work experience information from the resume"""
        experience_list = []
        experience_text = ""
        # Look for experience section under various possible headers
        for section_name, content in self.sections.items():
            if "EXPERIENCE" in section_name or "EMPLOYMENT" in section_name or "WORK" in section_name:
                experience_text = content
                break
        if not experience_text:
            return experience_list

        # Split the text into lines and group them into entries
        lines = experience_text.split('\n')
        entries = []
        current_entry = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Identify new entry by dates or job-related keywords
            date_pattern = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)?\s*\d{4}'
            if re.search(date_pattern, line) or any(keyword in line.lower() for keyword in ["intern", "engineer", "developer", "analyst"]):
                if current_entry:
                    entries.append('\n'.join(current_entry))
                current_entry = [line]
            else:
                current_entry.append(line)
        if current_entry:
            entries.append('\n'.join(current_entry))

        # Parse each entry into a structured dictionary
        for entry_text in entries:
            experience_entry = {
                "company": "", "position": "", "start_date": "", "end_date": "", "description": ""
            }
            entry_lines = entry_text.split('\n')
            # First line typically has position and dates
            if entry_lines:
                position_line = entry_lines[0]
                date_matches = re.findall(date_pattern, position_line)
                if len(date_matches) >= 2:
                    experience_entry["start_date"] = date_matches[0]
                    experience_entry["end_date"] = date_matches[1]
                elif len(date_matches) == 1:
                    experience_entry["end_date"] = date_matches[0]
                # Clean up the position by removing dates
                for date in date_matches:
                    position_line = position_line.replace(date, '')
                experience_entry["position"] = position_line.strip().rstrip('-–—')
            
            # Second line is assumed to be the company
            if len(entry_lines) > 1:
                experience_entry["company"] = entry_lines[1].strip()
            
            # Remaining lines are the description
            if len(entry_lines) > 2:
                experience_entry["description"] = '\n'.join(entry_lines[2:])

            # Add entry if it has meaningful content
            if experience_entry["position"] or experience_entry["company"]:
                experience_list.append(experience_entry)

        return experience_list
    
    def extract_projects(self) -> List[Dict[str, str]]:
        """Extract project information from the resume"""
        projects_list = []
        projects_text = ""
        for section_name, content in self.sections.items():
            if "PROJECT" in section_name:
                projects_text += content + "\n"
        if not projects_text:
            return projects_list
        tech_keywords = [
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "PHP", "Swift",
            "HTML", "CSS", "SQL", "NoSQL", "React", "Angular", "Vue", "Node.js", "Express",
            "Django", "Flask", "Spring", "ASP.NET", "Ruby on Rails", "Laravel",
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "Git"
        ]
        lines = projects_text.split('\n')
        entries = []
        current_entry = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if not line.startswith('•'):
                if current_entry:
                    entries.append('\n'.join(current_entry))
                current_entry = [line]
            else:
                current_entry.append(line)
        if current_entry:
            entries.append('\n'.join(current_entry))
        for entry_text in entries:
            if not entry_text.strip():
                continue
            project_entry = {
                "name": "", "description": "", "technologies": "", "url": ""
            }
            entry_lines = entry_text.split('\n')
            if entry_lines:
                project_entry["name"] = entry_lines[0].strip()
                if len(entry_lines) > 1:
                    project_entry["description"] = '\n'.join(entry_lines[1:])
            found_techs = []
            for tech in tech_keywords:
                if re.search(r'\b' + re.escape(tech) + r'\b', entry_text, re.IGNORECASE):
                    found_techs.append(tech)
            if found_techs:
                project_entry["technologies"] = ", ".join(found_techs)
            url_pattern = r'(?:github\.com|gitlab\.com|bitbucket\.org|herokuapp\.com|netlify\.app)/[\w.-]+/[\w.-]+'
            url_matches = re.findall(url_pattern, entry_text)
            if url_matches:
                project_entry["url"] = url_matches[0]
            projects_list.append(project_entry)
        return projects_list
    
    def extract_all(self) -> Dict[str, Any]:
        """Extract all information from the resume"""
        return {
            "contact_info": self.extract_contact_info(),
            "skills": self.extract_skills(),
            "education": self.extract_education(),
            "experience": self.extract_experience(),
            "projects": self.extract_projects()
        }