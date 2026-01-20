from typing import Dict, Any

def generate_cover_letter(resume_data: Dict[str, Any], jd_data: Dict[str, Any], tone: str = "formal") -> str:
    """
    Generates a cover letter based on resume and job description.
    Returns a deterministic dummy string.
    """
    return f"""Dear Hiring Manager,

I am writing to express my interest in the {jd_data.get('role', 'position')} role. 
With my experience in {', '.join(resume_data.get('extracted_skills', [])[:3])}, I believe I am a strong candidate.

I look forward to discussing my qualifications.

Sincerely,
[Candidate Name]"""
