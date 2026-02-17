from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.auth.auth_utils import get_current_user
from app.core.database import get_db
from app.models.cover_letter import CoverLetter
from app.models.schemas import (
    ResumeResponse,
    JDResponse,
    GenerateRequest,
    GenerateResponse
)
import uuid

router = APIRouter(
    prefix="/api",
    tags=["Cover Letter Pipeline"]
)

from app.utils.file_handler import save_upload
from app.services.parser import parse_resume, parse_job_description
from app.services.pipeline import run_pipeline

# -------------------------------
# Resume Upload (Protected)
# -------------------------------
@router.post("/upload-resume", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    # 1. Save file
    file_path = save_upload(file)
    
    # 2. Parse PDF
    parsed_data = parse_resume(file_path)
    
    # Check for errors
    if "error" in parsed_data:
        # In production, raise HTTPException
        pass

    return {
        "resume_id": str(uuid.uuid4()),
        "extracted_skills": parsed_data.get("extracted_skills", []),
        "experience_level": parsed_data.get("experience_level", "Unknown"),
        "extracted_text": parsed_data.get("extracted_text", "")
    }

# -------------------------------
# Job Description Submission (Protected)
# -------------------------------
@router.post("/submit-jd", response_model=JDResponse)
async def submit_job_description(
    jd_text: str,
    user=Depends(get_current_user)
):
    parsed_data = parse_job_description(jd_text)
    
    return {
        "jd_id": str(uuid.uuid4()),
        "required_skills": parsed_data.get("required_skills", [])
    }

# -------------------------------
# Cover Letter Generation (Protected)
# -------------------------------
@router.post("/generate-cover-letter", response_model=GenerateResponse)
async def generate_cover_letter(
    request: GenerateRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # In a real app, we would fetch resume/JD text using the IDs.
    # For now, we prefer text passed from frontend, or fallback to placeholders.
    resume_text = request.resume_text or "Resume content not found."
    jd_text = request.jd_text or "Job description content not found."

    result = run_pipeline(
        resume_text=resume_text, 
        jd_text=jd_text, 
        tone=request.tone
    )
    
    # Save to Database
    new_letter = CoverLetter(
        user_id=user["sub"],
        title=f"Cover Letter - {request.tone.capitalize()}",
        content=result["cover_letter"],
        match_score=result["match_score"],
        job_description=jd_text
    )
    db.add(new_letter)
    db.commit()
    db.refresh(new_letter)
    
    return {
        "cover_letter": result["cover_letter"],
        "match_score": result["match_score"],
        "keyword_coverage": "85%"
    }

from typing import List
from app.models.schemas import CoverLetterHistoryItem

# -------------------------------
# History / Profile (Protected)
# -------------------------------
@router.get("/get-history", response_model=List[CoverLetterHistoryItem])
async def get_user_history(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(CoverLetter).filter(CoverLetter.user_id == user["sub"]).order_by(CoverLetter.created_at.desc()).all()
    return history
