"""
dlp.py

Contains simple Data Loss Prevention redaction logic.

DLP helps prevent sensitive data from being sent to an LLM provider.
This file uses regular expressions to redact common sensitive values.
"""

import re


def redact_sensitive_data(text: str) -> str:
    """
    Redact basic sensitive data patterns from user input.

    Current examples:
    - Email addresses
    - AWS access key IDs
    - US SSN-like values

    Args:
        text: Original user prompt.

    Returns:
        Sanitized prompt with sensitive values replaced.
    """

    sanitized = text

    # Redact email addresses.
    sanitized = re.sub(
        r"[\w\.-]+@[\w\.-]+\.\w+",
        "[REDACTED_EMAIL]",
        sanitized,
    )

    # Redact AWS access key IDs.
    sanitized = re.sub(
        r"AKIA[0-9A-Z]{16}",
        "[REDACTED_AWS_ACCESS_KEY]",
        sanitized,
    )

    # Redact SSN-like values.
    sanitized = re.sub(
        r"\b\d{3}-\d{2}-\d{4}\b",
        "[REDACTED_SSN]",
        sanitized,
    )

    return sanitized
