"""
auth.py

Handles simple API key authentication and role checks.

This beginner version keeps demo API keys in code so the project is easy to run.
In production, API keys should be stored in a secure secrets manager.
"""

from typing import Dict, List

from fastapi import Header, HTTPException, status


# Demo API keys for local testing.
# Key string -> user identity and role.
API_KEYS = {
    "admin-demo-key": {
        "user_id": "admin-user",
        "role": "admin",
    },
    "user-demo-key": {
        "user_id": "demo-user",
        "role": "user",
    },
}


def get_current_user(x_api_key: str = Header(...)) -> Dict[str, str]:
    """
    Validate the API key from the request header.

    FastAPI automatically reads the HTTP header named "x-api-key"
    and passes it into this function.

    Args:
        x_api_key: API key sent by the client.

    Returns:
        Authenticated user identity.

    Raises:
        HTTPException: If the API key is invalid.
    """

    current_user = API_KEYS.get(x_api_key)

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return current_user


def require_role(current_user: Dict[str, str], allowed_roles: List[str]) -> None:
    """
    Check whether the authenticated user has one of the allowed roles.

    Args:
        current_user: User identity returned by get_current_user().
        allowed_roles: Roles that are allowed to access an endpoint.

    Raises:
        HTTPException: If the user does not have permission.
    """

    if current_user["role"] not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role is not allowed to access this endpoint",
        )
