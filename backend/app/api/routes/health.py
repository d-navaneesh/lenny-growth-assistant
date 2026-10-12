from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import get_settings
from app.db.session import SessionLocal

router = APIRouter(prefix="/health", tags=["health"])
settings = get_settings()


@router.get("")
async def health() -> dict:
    return {
        "status": "ok",
        "service": settings.app_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/ready")
async def ready() -> dict:
    try:
        with SessionLocal() as session:
            session.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False
    return {
        "status": "ok" if db_ok else "degraded",
        "database": "ready" if db_ok else "unavailable",
        "provider": settings.selected_provider,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
