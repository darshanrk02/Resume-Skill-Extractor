from typing import List
from ..models.resume import Skill

def extract_skills(text: str) -> List[Skill]:
    """Extract skills from text using keyword matching.
    
    Args:
        text: The text to extract skills from
        
    Returns:
        List of extracted skills as Skill objects
    """
    if not text:
        return []
        
    common_skills = [
        'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go',
        'django', 'flask', 'react', 'angular', 'vue', 'node.js', 'express', 'spring', 'laravel',
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'oracle', 'sql server',
        'docker', 'kubernetes', 'aws', 'azure', 'google cloud', 'devops', 'ci/cd',
        'git', 'github', 'gitlab', 'bitbucket', 'jenkins', 'ansible', 'terraform',
        'machine learning', 'deep learning', 'ai', 'data science', 'nlp', 'computer vision',
        'agile', 'scrum', 'kanban', 'project management'
    ]
    
    text_lower = text.lower()
    found_skills = [skill for skill in common_skills if skill in text_lower]
    
    # Convert to Skill objects
    skill_objects = [Skill(name=skill) for skill in sorted(set(found_skills))]
    return skill_objects
