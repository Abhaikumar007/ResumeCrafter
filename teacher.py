import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def enrich_cv_data(structured_data: dict) -> dict:
    """
    Uses Google Gemini as a pure creative writer. It uses simple placeholders for emphasis,
    and is FORBIDDEN from writing LaTeX code itself.
    """
    print("🧑‍🏫 [Teacher] Performing creative writing with simple placeholders...")
    data_string = json.dumps(structured_data, indent=2)

    prompt = f"""
    You are a top-tier tech resume strategist. Your job is creative writing, NOT code generation.

    ### YOUR CORE LOGIC ###
    Your task is to review the client's data and improve it.
    - If you see a `raw_notes` field, deconstruct it into a new, professional `description` list.
    - If you see an existing `description` list, evaluate each point: rewrite weak ones, but KEEP strong, quantified ones as they are.
    - Write a powerful new `summary` and professionally categorize the `skills`.

    ### CRITICAL RULES FOR YOUR OUTPUT ###
    1.  **USE PLACEHOLDERS FOR EMPHASIS (NON-NEGOTIABLE)**: When you want to emphasize a keyword, technology, or metric, you MUST wrap it in a special placeholder: `@@bold:text to bold@@`.
        - **Correct Example:** `...increased performance by @@bold:25%@@ using @@bold:Python@@.`
        - **INCORRECT:** `...increased performance by \\textbf{{25%}}...`

    2.  **DO NOT WRITE ANY LATEX CODE**: You are strictly FORBIDDEN from writing any LaTeX commands like `\\textbf`, `\\item`, etc. You are also FORBIDDEN from escaping special characters like `\\%` or `\\&`. A separate Python program will handle all of that. Just write clean, natural language with the `@@bold:...@@` placeholder where needed.

    3.  **KEEP `raw_notes`**: If the `raw_notes` field exists in the input, leave it in your output. Python will handle deleting it later.

    **CLIENT DATA TO TRANSFORM:**
    ---
    {data_string}
    ---

    Return ONLY the transformed JSON object.
    """
    
    try:
        model = genai.GenerativeModel(
            'models/gemini-1.5-flash-latest',
            generation_config={"response_mime_type": "application/json"}
        )
        response = model.generate_content(prompt)
        enriched_data = json.loads(response.text)
        print("✅ [Teacher] Creative writing complete.")
        return enriched_data
    except Exception as e:
        print(f"❌ [Teacher] Error during creative writing: {e}")
        return structured_data