from typing import Dict, Any, List

def parse_resume(resume_text: str) -> Dict[str, Any]:
    """
    Parses resume text and extracts key information.
    Returns deterministic dummy data.
    """
    return {
        "extracted_skills": ["Python", "FastAPI", "AWS", "Docker"],
        "experience_level": "Senior",
        "years_of_experience": 5,
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
    Returns deterministic dummy data.
    """
    return {
        "required_skills": ["Python", "FastAPI", "Cloud Computing"],
        "role": "Backend Engineer",
        "min_experience": 3
    }
