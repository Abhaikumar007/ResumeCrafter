import re

def _sanitize_string(text: str) -> str:
    """
    Sanitizes a single string to escape LaTeX special characters
    that are not already part of a command or escaped.
    """
    if not isinstance(text, str):
        return text

    # Use negative lookbehind `(?<!\\)` to match a character only if it's NOT preceded by a backslash.
    # This prevents double-escaping (e.g., turning `\%` into `\\%`).
    sanitized_text = text
    sanitized_text = re.sub(r'(?<!\\)&', r'\\&', sanitized_text)
    sanitized_text = re.sub(r'(?<!\\)%', r'\\%', sanitized_text)
    sanitized_text = re.sub(r'(?<!\\)\$', r'\\$', sanitized_text)
    sanitized_text = re.sub(r'(?<!\\)#', r'\\#', sanitized_text)
    sanitized_text = re.sub(r'(?<!\\)_', r'\\_', sanitized_text)
    
    return sanitized_text

def sanitize_for_latex(data):
    """
    Recursively traverses a dictionary or list and sanitizes all string values for LaTeX.
    """
    if isinstance(data, dict):
        # If it's a dictionary, sanitize each of its values
        return {key: sanitize_for_latex(value) for key, value in data.items()}
    elif isinstance(data, list):
        # If it's a list, sanitize each of its items
        return [sanitize_for_latex(item) for item in data]
    elif isinstance(data, str):
        # If it's a string, apply the sanitization function
        return _sanitize_string(data)
    else:
        # If it's another data type (int, bool, etc.), return it as is
        return data

def validate_latex_syntax(latex_code: str) -> list:
    """
    Performs basic syntax validation on the FINAL string of LaTeX code.
    This runs AFTER sanitization and generation.
    Returns a list of potential errors (warnings).
    """
    warnings = []
    if latex_code.count('{') != latex_code.count('}'):
        warnings.append("Mismatched curly braces {}. Check for unclosed commands like \\textbf{.")
    
    return warnings