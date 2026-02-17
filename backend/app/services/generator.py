from typing import Dict, Any

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')

def generate_cover_letter(resume_data: Dict[str, Any], jd_data: Dict[str, Any], tone: str = "formal") -> str:
    """
    Generates a cover letter based on resume and job description using Gemini.
    """
    try:
        if not os.getenv("GEMINI_API_KEY"):
            return "Error: GEMINI_API_KEY not found in environment variables."

        prompt = f"""
        You are an expert career coach. Write a {tone} cover letter for the following candidate applying for a job.
        
        RESUME DATA:
        {resume_data}
        
        JOB DESCRIPTION:
        {jd_data}
        
        Requirements:
        1. Tailor the content to the specific job requirements.
        2. Highlight relevant skills from the resume.
        3. Maintain a professional yet engaging tone.
        4. Do not include placeholders like "[Your Name]" if the name is available in the resume data.
        5. Keep it concise (under 400 words).
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"
