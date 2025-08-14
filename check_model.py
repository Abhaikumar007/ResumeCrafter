import google.generativeai as genai
import os
from dotenv import load_dotenv

print("--- 🔍 Checking available Gemini models for your API key... ---")

try:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in .env file.")
    else:
        genai.configure(api_key=api_key)
        
        print("✅ API key loaded. Fetching models...\n")
        
        found_generative_model = False
        for model in genai.list_models():
            # The 'generateContent' method is what we need for our script.
            if 'generateContent' in model.supported_generation_methods:
                print(f"✔️ Model found: {model.name}")
                found_generative_model = True
        
        if not found_generative_model:
            print("\n❌ CRITICAL: No models supporting 'generateContent' were found for your API key.")
            print("This usually means the 'Generative Language API' is not enabled in your Google Cloud project.")

except Exception as e:
    print(f"\n❌ An error occurred: {e}")
    print("Please double-check that your API key is correct and that the Generative Language API is enabled.")

print("\n--- ✅ Check complete ---")