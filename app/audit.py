"""
audit.py

Handles simple audit logging.

For this beginner version, logs are printed to the terminal.
In AWS, these logs would be visible in CloudWatch Logs.
"""

from datetime import datetime, timezone
from typing import Optional


def write_audit_log(
    user_id: str,
    role: str,
    action: str,
    status: str,
    reason: Optional[str] = None,
) -> None:
    """
    Write a simple structured audit log.

    Args:
        user_id: Authenticated user ID.
        role: User role.
        action: API action being performed.
        status: Security decision, such as "allowed" or "blocked".
        reason: Optional reason for the decision.
    """

    log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "role": role,
        "action": action,
        "status": status,
        "reason": reason,
    }

    print("AUDIT LOG:", log)
