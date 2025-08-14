from jinja2 import Environment, FileSystemLoader
import os

def generate_latex(enriched_data: dict, template_name: str = "modern_cv.tex") -> str:
    """
    Generates a LaTeX string from structured data using a Jinja2 template.
    """
    print("📝 [Generator] Generating LaTeX source from template...")
    
    # Setup Jinja2 environment with LaTeX-friendly delimiters
    env = Environment(
        loader=FileSystemLoader(searchpath="./templates"),
        block_start_string='\\block{',
        block_end_string='}',
        variable_start_string='\\var{',
        variable_end_string='}',
        comment_start_string='\\#{',
        comment_end_string='}',
        trim_blocks=True,
        autoescape=False
    )
    
    template = env.get_template(template_name)
    
    # Render the template with the data
    latex_output = template.render(enriched_data)
    
    print("✅ [Generator] LaTeX source generated successfully.")
    return latex_output