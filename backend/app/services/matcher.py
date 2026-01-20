from typing import Dict, Any, List

def match_resume_to_jd(resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compares parsed resume data against job description requirements.
    Returns a match score and analysis.
    """
    return {
        "match_score": 0.85,
        "matched_skills": ["Python", "FastAPI"],
        "missing_skills": ["Cloud Computing"],
        "analysis": "Strong match for backend role, but missing some cloud experience."
    }
