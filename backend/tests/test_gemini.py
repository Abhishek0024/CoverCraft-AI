import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
from app.services.generator import generate_cover_letter
import google.generativeai as genai
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Check if key is present
if not os.getenv("GEMINI_API_KEY"):
    print("❌ GEMINI_API_KEY not found in environment!")
    print("Please create a .env file with your API key.")
    exit(1)

# Dummy Data
resume_data = {
    "name": "Jane Doe",
    "extracted_skills": ["Python", "FastAPI", "React", "AWS"],
    "experience": "5 years as a Full Stack Developer"
}

jd_data = {
    "role": "Senior Software Engineer",
    "company": "TechCorp",
    "description": "Looking for a python expert with cloud experience."
}

print(f"Testing generation with API Key: {os.getenv('GEMINI_API_KEY')[:5]}...")

try:
    letter = generate_cover_letter(resume_data, jd_data)
    print("\n✅ Generation Successful!\n")
    print(letter[:200] + "...\n(truncated)")
except Exception as e:
    print(f"\n❌ Generation Failed: {e}")
