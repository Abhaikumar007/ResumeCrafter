import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- Gemini Change Start ---
load_dotenv()
# Configure the Gemini API client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# --- Gemini Change End ---

def parse_cv_data(raw_text: str) -> dict:
    """
    Uses Google Gemini to parse unstructured text into a structured CV data dictionary.
    """
    print("🧠 [Parser] Starting to parse raw text with Gemini...")

    # --- PROMPT CHANGE START ---
    # We are changing the schema for 'experience' and 'projects' to use 'raw_notes'.
    # This makes the parser's job simpler and more reliable.
    prompt = f"""
    You are an expert data extraction system. Your task is to parse the following raw text from a user's CV notes and convert it into a structured JSON object.

    The JSON object must have the following schema. For 'experience' and 'projects', capture all the descriptive text as a SINGLE STRING in the 'raw_notes' field.
    - "contact_info": {{ "name": "...", "phone": "...", "email": "...", "linkedin": "(username only)", "github": "(username only)" }}
    - "summary": "A short, raw summary string from the user. Do not make a new one."
    - "education": [ {{ "degree": "...", "university": "...", "dates": "...", "location": "..." }} ]
    - "certifications": [ {{ "name": "...", "date": "...", "issuer": "..." }} ]
    - "experience": [ {{ "title": "...", "company": "...", "dates": "...", "location": "...", "raw_notes": "A single string containing all user notes for this job." }} ]
    - "projects": [ {{ "name": "...", "raw_notes": "A single string of user notes.", "technologies": ["..."], "url": "..." }} ]
    - "skills": {{
        "Languages": ["..."],
        "Frameworks/Technologies": ["..."],
        "Databases": ["..."],
        "Tools": ["..."]
      }}

    If a section or field is not present in the text, omit it.

    Raw Text to Parse:
    ---
    {raw_text}
    ---

    Return ONLY the JSON object. Do not include any other text, markdown formatting like ```json, or explanations.
    """
    # --- PROMPT CHANGE END ---

    try:
        # --- Gemini Change Start ---
        model = genai.GenerativeModel(
            'models/gemini-1.5-flash-latest',
            generation_config={"response_mime_type": "application/json"} # This enables JSON mode
        )
        response = model.generate_content(prompt)
        
        # The response text contains the JSON string
        structured_data = json.loads(response.text)
        # --- Gemini Change End ---

        print("✅ [Parser] Successfully parsed text into structured data.")
        return structured_data
    except Exception as e:
        print(f"❌ [Parser] Error parsing CV data: {e}")
        return {}