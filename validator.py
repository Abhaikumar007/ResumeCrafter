import re

def post_process_for_latex(data):
    """
    The main post-processing function. It recursively traverses the data structure,
    converts custom placeholders to LaTeX, and then sanitizes the remaining text.
    """
    if isinstance(data, dict):
        return {key: post_process_for_latex(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [post_process_for_latex(item) for item in data]
    elif isinstance(data, str):
        # If it's a string, apply the full processing pipeline
        return _process_string_for_latex(data)
    else:
        # Not a string, dict, or list, so return it as is
        return data

def _sanitize_text_segment(segment: str) -> str:
    """A simple function to escape special characters in a piece of plain text."""
    if not segment:
        return ""
    segment = segment.replace('&', '\\&')
    segment = segment.replace('%', '\\%')
    segment = segment.replace('$', '\\$')
    segment = segment.replace('#', '\\#')
    segment = segment.replace('_', '\\_')
    return segment

def _process_string_for_latex(text: str) -> str:
    """
    A robust, pattern-based function to convert a string to safe LaTeX.
    This replaces the old, buggy implementation.
    """
    # Pattern to split the string by our placeholder, but KEEP the placeholder
    pattern = r'(@@bold:.*?@@)'
    parts = re.split(pattern, text)
    
    result_parts = []
    for part in parts:
        if part.startswith('@@bold:'):
            # This is a placeholder. Extract its content.
            # The content is from index 7 to the last 2 characters.
            content = part[7:-2]
            # Sanitize the content itself, in case it's something like "25%_profit"
            sanitized_content = _sanitize_text_segment(content)
            # Wrap the sanitized content in the LaTeX command
            result_parts.append(f"\\textbf{{{sanitized_content}}}")
        else:
            # This is a regular text segment. Sanitize it directly.
            result_parts.append(_sanitize_text_segment(part))
            
    # Join all the processed parts back into a single, safe string.
    return "".join(result_parts)

def validate_final_syntax(latex_code: str) -> list:
    """Performs a final, simple check on the fully compiled document."""
    warnings = []
    if latex_code.count('{') != latex_code.count('}'):
        warnings.append("Mismatched curly braces {}. This is a critical error.")
    return warnings