import re

def format_cover_letter(raw_text: str) -> str:
    """
    Post-processes the generated cover letter.
    Removes markdown code blocks and internal thought traces if any.
    """
    # Remove markdown code blocks
    cleaned_text = re.sub(r'```(?:markdown)?', '', raw_text)
    cleaned_text = cleaned_text.replace('```', '')
    
    # Remove common chat preambles (simple heuristic)
    # Use re.DOTALL to match across lines if needed, or just stripping first
    cleaned_text = re.sub(r'^\s*Here is a .* cover letter.*:', '', cleaned_text, flags=re.IGNORECASE | re.DOTALL)
    
    return cleaned_text.strip()
