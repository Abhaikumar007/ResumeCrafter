import os
import json
import cv_parser
import teacher
import latex_generator
import validator

def main():
    """
    Main function to run the CV generation workflow.
    """
    print("--- 🚀 Welcome to the AI Smart CV Generator 🚀 ---")

    # ... (Steps 1, 2 remain the same) ...

    input_file = "input.txt"
    output_tex_file = "output/cv_draft.tex"
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    print(f"\n[Step 1/7] Reading raw data from '{input_file}'...")

    print("\n[Step 2/7] Parsing data with AI Parser...")
    structured_data = cv_parser.parse_cv_data(raw_text)
    if not structured_data:
        print("❌ Halting process due to parsing failure.")
        return
    with open('output/1_parsed_data.json', 'w') as f:
        json.dump(structured_data, f, indent=2)

    print("\n[Step 3/7] Enriching data with AI Teacher...")
    enriched_data = teacher.enrich_cv_data(structured_data)
    with open('output/2_enriched_data.json', 'w') as f:
        json.dump(enriched_data, f, indent=2)

    # --- NEW RELIABILITY STEP ---
    print("\n[Step 4/7] Sanitizing AI output for LaTeX compatibility...")
    sanitized_data = validator.sanitize_for_latex(enriched_data)
    # Optional: Save this step to see the difference
    with open('output/3_sanitized_data.json', 'w') as f:
        json.dump(sanitized_data, f, indent=2)
    print("✅ Sanitization complete.")
    
    # --- END NEW STEP ---

    print("\n[Step 5/7] Generating LaTeX draft...")
    # IMPORTANT: Use the sanitized_data from now on
    latex_draft = latex_generator.generate_latex(sanitized_data)
    
    os.makedirs(os.path.dirname(output_tex_file), exist_ok=True)
    with open(output_tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_draft)
    print(f"✅ Draft saved to '{output_tex_file}'")

    print("\n[Step 6/7] Validating final LaTeX syntax...")
    warnings = validator.validate_latex_syntax(latex_draft)
    if not warnings:
        print("✅ Syntax validation passed with no obvious errors.")
    else:
        print("⚠️  Syntax validation found potential issues:")
        for warning in warnings:
            print(f"  - {warning}")

    print("\n[Step 7/7] Manual Edit & Finalization")
    print("-----------------------------------------")
    print("Your LaTeX draft has been generated.")
    print(f"👉 Please open '{output_tex_file}' and review it.")
    print("\nCompile it to a PDF using a LaTeX editor like Overleaf.")
    print("\n--- ✨ Process Complete ✨ ---")


if __name__ == "__main__":
    if not os.path.exists('output'):
        os.makedirs('output')
    main()