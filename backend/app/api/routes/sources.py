from __future__ import annotations

from fastapi import APIRouter

from app.retrieval.service import get_all_sources

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("")
async def list_sources() -> dict:
    sources = get_all_sources()
    return {"items": [{"title": item["title"], "url": item.get("url"), "author": item.get("author"), "episode": item.get("episode")} for item in sources]}
