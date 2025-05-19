from typing import Dict, Any, Optional, List, Union, BinaryIO
import os
import tempfile
import PyPDF2
import docx2txt
import io
from pathlib import Path
from fastapi import UploadFile
from ..models.resume import ResumeData, ContactInfo, Education, Experience, Project

async def extract_text_from_file(file_path: str, file_type: str) -> str:
    """Extract text from a file based on its type."""
    try:
        if file_type == 'pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return '\n'.join(page.extract_text() for page in reader.pages if page.extract_text())
        
        elif file_type in ['doc', 'docx']:
            return docx2txt.process(file_path)
        
        # Fallback to plain text
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    except Exception as e:
        raise ValueError(f"Error extracting text from {file_type} file: {str(e)}")

from ..utils.text_utils import extract_skills

def parse_contact_info(text: str) -> ContactInfo:
    """Extract contact information from resume text."""
    # This is a simplified example - in a real app, use more sophisticated parsing
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    email = next((line for line in lines if '@' in line and '.' in line.split('@')[1]), '')
    phone = next((line for line in lines if any(c.isdigit() for c in line) and 
                 sum(c.isdigit() for c in line) >= 10), '')
    
    return ContactInfo(
        email=email,
        phone=phone,
        name=lines[0] if lines else 'Unknown',
        linkedin='',
        github=''
    )

async def parse_resume(file_path: str, file_type: str) -> ResumeData:
    """
    Parse a resume file and return structured data.
    
    Args:
        file_path: Path to the resume file
        file_type: Type of the file (pdf, docx, etc.)
        
    Returns:
        ResumeData: Structured resume data
    """
    # Extract text from the file
    text = await extract_text_from_file(file_path, file_type)
    
    # Extract structured information
    contact_info = parse_contact_info(text)
    skills = extract_skills(text)
    
    # Create and return the ResumeData object
    return ResumeData(
        contact_info=contact_info,
        summary="",  # You can extract this from the resume
        skills=skills,
        experience=[],  # You can parse this from the resume
        education=[],   # You can parse this from the resume
        projects=[],    # You can parse this from the resume
        raw_text=text,
        file_name=os.path.basename(file_path),
        file_type=file_type,
        file_size=os.path.getsize(file_path)
    )

async def parse_uploaded_resume(file: UploadFile) -> ResumeData:
    """
    Handle an uploaded resume file and parse its contents.
    
    Args:
        file: Uploaded file from FastAPI
        
    Returns:
        ResumeData: Parsed resume data
    """
    # Get file extension
    file_extension = Path(file.filename).suffix.lower().lstrip('.')
    if file_extension not in ['pdf', 'doc', 'docx', 'txt']:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
        # Read the uploaded file content
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        # Parse the resume
        return await parse_resume(temp_file_path, file_extension)
    except Exception as e:
        raise ValueError(f"Error parsing resume: {str(e)}")
    finally:
        # Clean up the temporary file
        try:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        except Exception as e:
            pass  # Log this in production
