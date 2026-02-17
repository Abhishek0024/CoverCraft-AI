from typing import Dict, Any, List

import os
from pypdf import PdfReader

def parse_resume(file_path_or_text: str) -> Dict[str, Any]:
    """
    Parses resume text from a PDF file OR raw text and extracts key information.
    """
    text = ""
    # Check if input is a file path
    if os.path.exists(file_path_or_text) and os.path.isfile(file_path_or_text):
        try:
            reader = PdfReader(file_path_or_text)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return {"error": "Failed to read PDF"}
    else:
        # Assume it's raw text
        text = file_path_or_text

    # Basic keyword extraction (This can be improved with LLM later)
    # For now, we return the raw text + some dummy extraction
    return {
        "extracted_text": text,
        "extracted_skills": ["Python", "FastAPI", "AWS", "Docker"], # Placeholder
        "experience_level": "Senior", # Placeholder
        "years_of_experience": 5, # Placeholder
        "education": [
            {
                "degree": "B.S. Computer Science",
                "institution": "University of Tech",
                "year": 2020
            }
        ]
    }

def parse_job_description(jd_text: str) -> Dict[str, Any]:
    """
    Parses job description text and extracts requirements.
    """
    return {
        "extracted_text": jd_text,
        "required_skills": [] # Could use simple keyword extraction here too if needed
    }
