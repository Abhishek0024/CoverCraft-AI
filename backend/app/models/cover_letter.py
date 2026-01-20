from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.user import Base
import uuid

class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    
    title = Column(String, default="Untitled Cover Letter")
    content = Column(Text)
    job_description = Column(Text) # Storing JD snapshot
    match_score = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    owner = relationship("User", back_populates="cover_letters")
