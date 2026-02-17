import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.matcher import match_resume_to_jd
from app.services.parser import parse_job_description, parse_resume
from app.services.postprocess import format_cover_letter

def test_services():
    print("Testing Helper Services...")

    # 1. Test Matcher
    resume_text = "I am a Python Developer with experience in FastAPI and Docker."
    jd_text = "Looking for a Python Developer who knows FastAPI, Docker, and Kubernetes."
    
    resume_data = {"extracted_text": resume_text}
    jd_data = {"extracted_text": jd_text}
    
    match_result = match_resume_to_jd(resume_data, jd_data)
    print(f"\n[Matcher] Score: {match_result['match_score']}")
    print(f"[Matcher] Matched: {match_result['matched_skills']}")
    print(f"[Matcher] Missing: {match_result['missing_skills']}")
    
    expected_matched = {'python', 'fastapi', 'docker'}
    assert set(match_result['matched_skills']) == expected_matched, "Matcher failed to find correct skills"
    
    # 2. Test Postprocess
    raw_letter = """
    Here is a generated cover letter:
    
    ```markdown
    Dear Hiring Manager,
    
    I am writing to apply...
    ```
    """
    cleaned = format_cover_letter(raw_text=raw_letter)
    print(f"\n[Postprocess] Cleaned start: {cleaned[:20]}...")
    assert "Here is" not in cleaned
    assert "```" not in cleaned
    assert "Dear Hiring Manager" in cleaned
    
    print("\n✅ All Service Tests Passed!")

if __name__ == "__main__":
    try:
        test_services()
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
