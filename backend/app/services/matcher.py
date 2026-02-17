import re
from typing import Dict, Any, List

def extract_keywords(text: str) -> set:
    """Simple keyword extraction using regex."""
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter for common tech keywords (this is a naive list for demo purposes)
    tech_keywords = {
        "python", "java", "react", "aws", "docker", "kubernetes", "sql", "nosql",
        "fastapi", "django", "flask", "javascript", "typescript", "html", "css",
        "git", "linux", "agile", "scrum", "cloud", "azure", "gcp", "devops",
        "ci/cd", "rest", "api", "graphql", "machine learning", "ai"
    }
    return {w for w in words if w in tech_keywords}

def match_resume_to_jd(resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compares parsed resume data against job description requirements.
    Calculates a match score based on keyword overlap.
    """
    resume_text = resume_data.get("extracted_text", "")
    jd_text = jd_data.get("extracted_text", "") # Assuming parser returns this

    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    # Calculate overlaps
    matched_skills = resume_keywords.intersection(jd_keywords)
    missing_skills = jd_keywords.difference(resume_keywords)
    
    # Calculate score
    if not jd_keywords:
        score = 0.5 # Default if no keywords found in JD
    else:
        score = len(matched_skills) / len(jd_keywords)
    
    # Analyze
    analysis = f"Matched {len(matched_skills)} out of {len(jd_keywords)} key terms."
    if missing_skills:
        analysis += f" Missing: {', '.join(list(missing_skills)[:5])}."

    return {
        "match_score": round(score, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "analysis": analysis
    }
