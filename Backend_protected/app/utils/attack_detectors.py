import re
from html import escape
from ..utils.loguru_config import logger  # Import logger for logging


# Compile patterns once and reuse
XSS_PATTERNS = [
    re.compile(r"<.*?>", re.IGNORECASE),
    re.compile(r"javascript:.*", re.IGNORECASE),
    re.compile(r"on\w+=\".*?\"", re.IGNORECASE),
    re.compile(r"&[a-zA-Z]+;", re.IGNORECASE),
]

SQL_PATTERNS = [
    re.compile(r"(--|;|/*|\*/|\\x27|\\x22|\\x2f\\x2a)", re.IGNORECASE),
    re.compile(r"(['\"]\s*(OR|AND)\s*['\"]|(['\"]\s*=\s*['\"]))", re.IGNORECASE),
    re.compile(r"(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|EXEC).*", re.IGNORECASE),
    re.compile(r"\b(\d+\s*=\s*\d+)\b", re.IGNORECASE),
]



def contains_xss(value: str) -> bool:
    if not value:
        return False
    for pattern in XSS_PATTERNS:
        if pattern.search(value):
            logger.warning(f"XSS pattern detected: {pattern.pattern} in value: {value}")
            return True
    return False



def contains_sql_injection(value: str) -> bool:
    if not value:
        return False
    for pattern in SQL_PATTERNS:
        if pattern.search(value):
            logger.warning(f"SQL Injection pattern detected: {pattern.pattern} in value: {value}")
            return True
    return False




def sanitize_input(input_value: str) -> str:
    """
    Escapes special characters in the input to prevent XSS attacks.
    Logs both the original and sanitized input for debugging.
    """
    logger.debug(f"Sanitizing input: {input_value}")
    if not isinstance(input_value, str):
        logger.error("Input for sanitization is not a string.")
        raise ValueError("Input must be a string.")
    sanitized_value = escape(input_value)
    if sanitized_value != input_value:
        logger.debug(f"Sanitized input: Original: {input_value}, Sanitized: {sanitized_value}")
    else:
        logger.debug(f"Input --> {input_value} is valid!")
    return sanitized_value




def prevent_sql_injection(input_value: str) -> str:
    """
    Detects and sanitizes SQL Injection attempts by removing dangerous keywords and characters.
    Logs any potential SQL injection patterns found in the input.
    """
    logger.debug(f"Checking for SQL injection in input: {input_value}")
    if not isinstance(input_value, str):
        logger.error("Input for SQL injection prevention is not a string.")
        raise ValueError("Input must be a string.")

    # List of SQL keywords and patterns to block
    dangerous_patterns = [
        r"(?i)(\bSELECT\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b|\bDROP\b|\bALTER\b|\bCREATE\b|\bEXEC\b|\bUNION\b|\b--\b|\b;\b|\bOR\b|\bAND\b)",
        r"(--|;|\\'|\\\")"  # SQL special characters
    ]

    sanitized_value = input_value
    for pattern in dangerous_patterns:
        if re.search(pattern, sanitized_value):
            logger.warning(f"Potential SQL injection pattern detected in {sanitized_value}")
        sanitized_value = re.sub(pattern, "", sanitized_value)

    logger.debug(f"SQL-safe input: Original: {input_value}, Sanitized: {sanitized_value}")
    return sanitized_value


