import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def enrich_cv_data(structured_data: dict) -> dict:
    """
    Uses Google Gemini as a conditional evaluator and improver. It fixes bad
    bullet points and leaves good ones untouched.
    """
    print("🧑‍🏫 [Teacher] Performing conditional evaluation and improvement...")
    data_string = json.dumps(structured_data, indent=2)

    prompt = f"""
    You are a top-tier tech resume strategist. Your goal is to ensure every job and project has world-class achievement bullet points. You will receive items that have EITHER a messy 'raw_notes' field OR an existing 'description' list. You must intelligently process both cases.

    ---
    ### YOUR CORE LOGIC AND EXAMPLES ###

    #### CASE 1: You receive 'raw_notes' (a messy string).
    Your task is to deconstruct it into a new, professional 'description' list.
    **Input Example:**
    {{ "raw_notes": "i did the frontend with library X, also built the REST apis and fixed some database issues." }}
    **Required Output:**
    {{ "description": [
        "Developed a dynamic user interface using \\textbf{{Library X}}, improving user engagement.",
        "Engineered backend RESTful APIs and optimized database queries to reduce server response time by \\textbf{{30%}}."
      ]
    }}

    #### CASE 2: You receive 'description' (an existing list of bullet points).
    Your task is to evaluate EACH bullet point. If it's weak, rewrite it. If it's already strong, KEEP IT AS IS.
    **Input Example:**
    {{ "description": [
        "Reduced API latency by 40% through query optimization.",
        "wrote code for the backend",
        "Participated in daily stand-up meetings."
      ]
    }}
    **Your Thinking Process for Evaluation:**
    1.  "Reduced API latency...": This is a great bullet point. It's quantified and uses an action verb. I will keep it.
    2.  "wrote code for the backend": This is weak. It's passive and lacks detail. I must rewrite it.
    3.  "Participated in meetings...": This is a low-value activity, not an achievement. I must rewrite it to show impact, or remove it if it adds no value.
    **Required Output:**
    {{ "description": [
        "Reduced API latency by 40% through query optimization.",
        "Developed and maintained scalable backend services using \\textbf{{Node.js}} to support core application features.",
        "Collaborated in an Agile environment, contributing to daily stand-ups to streamline development cycles and resolve blockers."
      ]
    }}
    ---

    ### FINAL INSTRUCTIONS ###
    1.  **APPLY THE LOGIC**: Apply the correct logic (CASE 1 or CASE 2) to every item in 'experience' and 'projects'. The final output for each item must have a 'description' field.
    2.  **IMPROVE OTHER SECTIONS**: Also write a new, powerful 'summary' and professionally categorize the 'skills'.
    3.  **LATEX FORMATTING**: Ensure correct `\\textbf{{}}` and special character escaping (`\\%`, `\\&`, etc.) in all rewritten points.
    4.  **CLEANUP**: Leave the `raw_notes` field if it exists. Python will handle removing it.

    **CLIENT DATA TO TRANSFORM:**
    ---
    {data_string}
    ---

    Return ONLY the transformed JSON object. No explanations.
    """
    
    try:
        model = genai.GenerativeModel(
            'models/gemini-1.5-flash-latest',
            generation_config={"response_mime_type": "application/json"}
        )
        response = model.generate_content(prompt)
        enriched_data = json.loads(response.text)
        print("✅ [Teacher] Conditional improvement complete.")
        return enriched_data
    except Exception as e:
        print(f"❌ [Teacher] Error during conditional improvement: {e}")
        return structured_data