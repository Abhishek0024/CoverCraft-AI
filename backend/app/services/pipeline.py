from app.services.parser import parse_resume, parse_job_description
from app.services.matcher import match_resume_to_jd
from app.services.generator import generate_cover_letter
from app.services.postprocess import format_cover_letter
from typing import Dict, Any

def run_pipeline(resume_text: str, jd_text: str, tone: str = "formal") -> Dict[str, Any]:
    """
    Orchestrates the full cover letter generation pipeline.
    """
    # 1. Parse Inputs
    resume_data = parse_resume(resume_text)
    jd_data = parse_job_description(jd_text)

    # 2. Match Resume to JD
    match_result = match_resume_to_jd(resume_data, jd_data)

    # 3. Generate Cover Letter
    raw_letter = generate_cover_letter(resume_data, jd_data, tone)

    # 4. Post-process
    final_letter = format_cover_letter(raw_letter)

    return {
        "cover_letter": final_letter,
        "match_score": match_result["match_score"],
        "analysis": match_result["analysis"]
    }
