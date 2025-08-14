import os
import json
import cv_parser
import teacher
import latex_generator
import validator

def cleanup_raw_notes(data: dict) -> dict:
    """
    Reliably removes the 'raw_notes' field after the AI has used it.
    """
    if 'experience' in data:
        for item in data['experience']:
            if 'raw_notes' in item:
                del item['raw_notes']
    if 'projects' in data:
        for item in data['projects']:
            if 'raw_notes' in item:
                del item['raw_notes']
    return data

def main():
    """
    Main function to run the CV generation workflow.
    """
    print("--- 🚀 Welcome to the AI Smart CV Generator 🚀 ---")

    input_file = "input.txt"
    output_tex_file = "output/cv_draft.tex"
    
    # Step 1: Read Input
    print(f"\n[Step 1/8] Reading raw data from '{input_file}'...")
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Step 2: Parse
    print("\n[Step 2/8] Parsing data with AI Parser...")
    structured_data = cv_parser.parse_cv_data(raw_text)
    if not structured_data: return
    with open('output/1_parsed_data.json', 'w') as f: json.dump(structured_data, f, indent=2)

    # Step 3: Enrich with AI Teacher (Creative Writing)
    print("\n[Step 3/8] Enriching data with AI Teacher...")
    enriched_data = teacher.enrich_cv_data(structured_data)
    with open('output/2_enriched_data.json', 'w') as f: json.dump(enriched_data, f, indent=2)

    # Step 4: Post-Process with Python (Code Generation & Sanitization)
    print("\n[Step 4/8] Post-processing AI output into valid LaTeX...")
    processed_data = validator.post_process_for_latex(enriched_data)
    print("✅ Placeholders converted and special characters sanitized.")
    
    # Step 5: Cleanup with Python
    print("\n[Step 5/8] Cleaning up intermediate data...")
    final_data = cleanup_raw_notes(processed_data)
    with open('output/3_final_data.json', 'w') as f: json.dump(final_data, f, indent=2)
    
    # Step 6: Generate LaTeX
    print("\n[Step 6/8] Generating LaTeX draft...")
    latex_draft = latex_generator.generate_latex(final_data)
    os.makedirs(os.path.dirname(output_tex_file), exist_ok=True)
    with open(output_tex_file, 'w', encoding='utf-8') as f: f.write(latex_draft)
    print(f"✅ Draft saved to '{output_tex_file}'")

    # Step 7: Validate Final Syntax
    print("\n[Step 7/8] Validating final LaTeX syntax...")
    warnings = validator.validate_final_syntax(latex_draft)
    if not warnings:
        print("✅ Syntax validation passed with no obvious errors.")
    else:
        for warning in warnings: print(f"  - {warning}")

    # Step 8: Finalization
    print("\n[Step 8/8] Manual Edit & Finalization")
    print("-----------------------------------------")
    print(f"👉 Your final, improved draft is ready at '{output_tex_file}'.")
    print("\nCompile it to a PDF using a LaTeX editor like Overleaf.")
    print("\n--- ✨ Process Complete ✨ ---")


if __name__ == "__main__":
    if not os.path.exists('output'): os.makedirs('output')
    main()