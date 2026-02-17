import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import os
import json

BASE_URL = "http://127.0.0.1:8000"
# We assume the server is running. If not, this test will fail to connect.
# However, I can also import the service functions directly to test logic without server.
# Let's test the Logic directly to avoid dependency on running server.

from app.services.parser import parse_resume
from app.services.pipeline import run_pipeline
from app.models.schemas import GenerateRequest
import uuid

# 1. Create a dummy PDF
from reportlab.pdfgen import canvas
pdf_path = "test_resume.pdf"
c = canvas.Canvas(pdf_path)
c.drawString(100, 750, "John Doe")
c.drawString(100, 730, "Experienced Python Developer with 5 years in AWS and FastAPI.")
c.drawString(100, 710, "Skills: Python, React, SQL, Docker")
c.save()

print("✅ Created dummy PDF")

# 2. Test Parser
try:
    parsed = parse_resume(pdf_path)
    print("✅ Parser Output:", parsed.keys())
    print("   Text snippet:", parsed.get("extracted_text", "")[:50])
except Exception as e:
    print(f"❌ Parser Failed: {e}")
    exit(1)

# 3. Test Generator Pipeline
jd_text = "Looking for a Senior Python Developer with AWS experience."
print("\nTesting Generator Pipeline with extracted text...")

try:
    # Mimic the route logic
    resume_text = parsed.get("extracted_text", "")
    res = run_pipeline(resume_text, jd_text, tone="formal")
    print("✅ Pipeline Success!")
    print("   Match Score:", res["match_score"])
    print("   Letter Snippet:", res["cover_letter"][:100])
except Exception as e:
    print(f"❌ Pipeline Failed: {e}")
    
# Clean up
if os.path.exists(pdf_path):
    os.remove(pdf_path)
