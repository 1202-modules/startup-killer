import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.config import get_settings
from backend.app.db.models import BrowserInstallation, GameSession
from backend.app.db.session import get_db

settings = get_settings()


def generate_csrf_token(installation_id: uuid.UUID) -> str:
    """Generates a deterministic HMAC-SHA256 CSRF token for a given installation ID."""
    return hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        f"csrf:{installation_id}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_csrf_token(csrf_token: str, installation_id: uuid.UUID) -> bool:
    """Verifies a CSRF token against expected HMAC using constant time comparison."""
    if not csrf_token:
        return False
    expected = generate_csrf_token(installation_id)
    return hmac.compare_digest(csrf_token, expected)


def get_optional_installation(
    request: Request,
    db: Session = Depends(get_db),
) -> Optional[BrowserInstallation]:
    """Retrieves BrowserInstallation if sk_browser cookie is present and valid."""
    raw_token = request.cookies.get(settings.COOKIE_NAME)
    if not raw_token:
        return None

    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    installation = db.scalar(
        select(BrowserInstallation).where(BrowserInstallation.token_hash == token_hash)
    )
    if installation:
        now = datetime.now(timezone.utc)
        last_seen = installation.last_seen_at
        if last_seen.tzinfo is None:
            last_seen = last_seen.replace(tzinfo=timezone.utc)
        if (now - last_seen).total_seconds() > 60:
            installation.last_seen_at = now
            db.commit()
    return installation


def get_or_create_installation(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> BrowserInstallation:
    """Retrieves existing BrowserInstallation or creates a new one and sets sk_browser cookie."""
    installation = get_optional_installation(request, db)
    if installation:
        return installation

    # Generate new cryptographically secure token
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    installation = BrowserInstallation(
        token_hash=token_hash,
        created_at=datetime.now(timezone.utc),
        last_seen_at=datetime.now(timezone.utc),
    )
    db.add(installation)
    db.commit()
    db.refresh(installation)

    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=raw_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        path="/",
        max_age=365 * 24 * 3600,
    )

    return installation


def get_current_installation(
    request: Request,
    db: Session = Depends(get_db),
) -> BrowserInstallation:
    """Requires an existing valid BrowserInstallation; raises 401 if missing."""
    installation = get_optional_installation(request, db)
    if not installation:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Требуется сессионная cookie sk_browser",
                "retryable": False,
            },
        )
    return installation


def require_csrf(
    request: Request,
    installation: BrowserInstallation = Depends(get_current_installation),
) -> None:
    """Validates X-CSRF-Token header against current installation."""
    token = request.headers.get("X-CSRF-Token")
    if not token or not verify_csrf_token(token, installation.id):
        raise HTTPException(
            status_code=403,
            detail={
                "code": "CSRF_INVALID",
                "message": "Недействительный или отсутствующий CSRF-токен",
                "retryable": False,
            },
        )


def require_idempotency_key(
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
) -> uuid.UUID:
    """Requires and validates Idempotency-Key header as a valid UUID."""
    if not idempotency_key:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "IDEMPOTENCY_KEY_REQUIRED",
                "message": "Заголовок Idempotency-Key обязателен",
                "retryable": False,
            },
        )
    try:
        return uuid.UUID(idempotency_key.strip())
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=422,
            detail={
                "code": "INVALID_IDEMPOTENCY_KEY",
                "message": "Заголовок Idempotency-Key должен содержать валидный UUID",
                "retryable": False,
            },
        )


def get_session_with_ownership(
    session_id: uuid.UUID,
    installation: BrowserInstallation = Depends(get_current_installation),
    db: Session = Depends(get_db),
) -> GameSession:
    """Retrieves session and verifies that it belongs to the current browser installation."""
    session = db.scalar(
        select(GameSession).where(GameSession.id == session_id)
    )
    if not session:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "SESSION_NOT_FOUND",
                "message": "Игровая сессия не найдена",
                "retryable": False,
            },
        )
    if session.browser_installation_id != installation.id:
        raise HTTPException(
            status_code=403,
            detail={
                "code": "SESSION_FORBIDDEN",
                "message": "Доступ к чужой игровой сессии запрещён",
                "retryable": False,
            },
        )
    return session
