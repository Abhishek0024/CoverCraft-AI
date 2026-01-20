from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# ===============================
# Authentication Schemas
# ===============================

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfile(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


# ===============================
# Resume & Job Description Schemas
# ===============================

class ResumeResponse(BaseModel):
    resume_id: str
    extracted_skills: List[str]
    experience_level: str


class JDResponse(BaseModel):
    jd_id: str
    required_skills: List[str]


# ===============================
# Cover Letter Generation Schemas
# ===============================

class GenerateRequest(BaseModel):
    resume_id: str
    jd_id: str
    tone: str              # e.g., formal, enthusiastic
    focus: str             # e.g., skills, achievements, culture


class GenerateResponse(BaseModel):
    cover_letter: str
    match_score: float
    keyword_coverage: str


# ===============================
# Optional (Future-Ready) Schemas
# ===============================

class MatchAnalysis(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    match_score: float


class SavedCoverLetter(BaseModel):
    letter_id: str
    resume_id: str
    jd_id: str
    tone: str
    created_at: str

class CoverLetterHistoryItem(BaseModel):
    id: str
    title: str
    content: str
    match_score: Optional[float]
    created_at: datetime  # datetime

    class Config:
        orm_mode = True
