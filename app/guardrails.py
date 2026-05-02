"""
guardrails.py

Contains simple prompt injection detection logic.

Prompt injection is when a user tries to override the system or developer
instructions given to an LLM. This file uses beginner-friendly keyword matching.
"""

from typing import Optional, Tuple


# Simple suspicious phrases for local testing.
# This is intentionally basic so the logic is easy to understand.
BLOCKED_PHRASES = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "reveal the system prompt",
    "reveal your system prompt",
    "show hidden instructions",
    "bypass all safety",
    "disable all restrictions",
    "developer mode",
    "forget all previous rules",
    "act as an unrestricted ai",
]


def detect_prompt_injection(prompt: str) -> Tuple[bool, Optional[str]]:
    """
    Check whether a prompt contains suspicious prompt injection phrases.

    Args:
        prompt: User input sent to the API.

    Returns:
        Tuple:
            - bool: True if blocked, False if allowed.
            - Optional[str]: The matched suspicious phrase, if found.
    """

    normalized_prompt = prompt.lower()

    for phrase in BLOCKED_PHRASES:
        if phrase in normalized_prompt:
            return True, phrase

    return False, None
