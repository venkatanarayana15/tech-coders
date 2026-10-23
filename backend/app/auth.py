from __future__ import annotations

from fastapi import Depends, HTTPException, Request, Response
from itsdangerous import BadSignature, URLSafeSerializer
from sqlmodel import Session

from .config import settings
from .db import get_session
from .models import User

COOKIE_NAME = "prism_session"
_SERIALIZER = URLSafeSerializer(settings.secret_key, salt="prismcheck-session")


def set_session(response: Response, user_id: str) -> None:
    response.set_cookie(
        COOKIE_NAME,
        _SERIALIZER.dumps({"uid": user_id}),
        max_age=60 * 60 * 24 * 7,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        path="/",
    )


def clear_session(response: Response) -> None:
    response.delete_cookie(COOKIE_NAME, path="/")


def session_user(request: Request, session: Session) -> User | None:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    try:
        payload = _SERIALIZER.loads(token)
    except BadSignature:
        return None
    user_id = payload.get("uid")
    return session.get(User, user_id) if user_id else None


def current_user(
    request: Request, session: Session = Depends(get_session)
) -> User:
    user = session_user(request, session)
    if user is None:
        raise HTTPException(status_code=401, detail="Sign in to continue.")
    return user


def require_role(user: User, *roles: str) -> None:
    if user.role not in roles:
        raise HTTPException(
            status_code=403,
            detail=f"This action needs one of these roles: {', '.join(roles)}.",
        )
