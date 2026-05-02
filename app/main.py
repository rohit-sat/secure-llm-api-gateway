"""
main.py

Main FastAPI application for the Secure LLM API Gateway.

This version is beginner-friendly and includes:
- Health check endpoint
- API key authentication
- Role-based access check
- Prompt injection detection
- Sensitive data redaction
- Audit logging
- Safe error handling for easier debugging
"""

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.audit import write_audit_log
from app.auth import get_current_user, require_role
from app.dlp import redact_sensitive_data
from app.guardrails import detect_prompt_injection


app = FastAPI(
    title="Secure LLM API Gateway",
    description="A beginner-friendly API showing basic AI security controls.",
    version="1.0.0",
)


class PromptRequest(BaseModel):
    """
    Request body expected by /secure-chat.

    Example:
        {
            "prompt": "Explain AWS IAM"
        }
    """

    prompt: str = Field(
        ...,
        min_length=1,
        description="User prompt sent to the LLM gateway",
    )


@app.get("/health")
def health_check() -> dict:
    """
    Basic health check endpoint.

    Returns:
        dict: API status.
    """

    return {
        "status": "ok",
        "message": "Secure LLM API Gateway is running",
    }


@app.post("/secure-chat")
def secure_chat(
    request: PromptRequest,
    current_user: dict = Depends(get_current_user),
) -> dict:
    """
    Securely process a user prompt before sending it to an LLM.

    Flow:
    1. User is authenticated by API key.
    2. User role is checked.
    3. Prompt is checked for prompt injection.
    4. Sensitive data is redacted.
    5. Audit log is written.
    6. Mock LLM response is returned.
    """

    try:
        # Step 1: Only admin and user roles can use this endpoint.
        require_role(current_user, allowed_roles=["admin", "user"])

        # Step 2: Check prompt for suspicious prompt injection phrases.
        is_blocked, reason = detect_prompt_injection(request.prompt)

        if is_blocked:
            write_audit_log(
                user_id=current_user.get("user_id", "unknown"),
                role=current_user.get("role", "unknown"),
                action="secure-chat",
                status="blocked",
                reason=reason or "prompt injection detected",
            )

            raise HTTPException(
                status_code=400,
                detail=f"Prompt blocked because it matched suspicious phrase: {reason}",
            )

        # Step 3: Redact sensitive data before the prompt reaches an LLM.
        sanitized_prompt = redact_sensitive_data(request.prompt)

        # Step 4: Log the allowed request.
        write_audit_log(
            user_id=current_user.get("user_id", "unknown"),
            role=current_user.get("role", "unknown"),
            action="secure-chat",
            status="allowed",
            reason="none",
        )

        # Step 5: Return mock LLM response.
        return {
            "status": "allowed",
            "user_id": current_user.get("user_id", "unknown"),
            "role": current_user.get("role", "unknown"),
            "sanitized_prompt": sanitized_prompt,
            "mock_llm_response": "This is where the LLM response would appear.",
        }

    except HTTPException:
        # Keep intentional FastAPI errors as-is.
        raise

    except Exception as error:
        # Print real error in terminal for debugging.
        print("ERROR in /secure-chat:", str(error))

        raise HTTPException(
            status_code=500,
            detail="Internal server error. Check terminal logs for details.",
        )
