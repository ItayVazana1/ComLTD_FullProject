import re
from html import escape

def sanitize_input(input_value: str) -> str:
    """
    Escapes special characters in the input to prevent XSS attacks.
    """
    if not isinstance(input_value, str):
        raise ValueError("Input must be a string.")
    return escape(input_value)

def prevent_sql_injection(input_value: str) -> str:
    """
    Detects and sanitizes SQL Injection attempts by removing dangerous keywords and characters.
    """
    if not isinstance(input_value, str):
        raise ValueError("Input must be a string.")

    # List of SQL keywords and patterns to block
    dangerous_patterns = [
        r"(?i)(\bSELECT\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b|\bDROP\b|\bALTER\b|\bCREATE\b|\bEXEC\b|\bUNION\b|\b--\b|\b;\b|\bOR\b|\bAND\b)",
        r"(--|;|\\'|\\\")"  # SQL special characters
    ]

    for pattern in dangerous_patterns:
        input_value = re.sub(pattern, "", input_value)

    return input_value

# Example usage:
# sanitized_input = sanitize_input("<script>alert('XSS')</script>")
# sql_safe_input = prevent_sql_injection("DROP TABLE users; --")
