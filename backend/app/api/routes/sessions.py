from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.db.models import Conversation, Message
from app.db.session import SessionLocal

router = APIRouter(prefix="/sessions", tags=["sessions"])


class SessionCreateRequest(BaseModel):
    title: str = Field(default="New conversation")
    owner: str | None = None


@router.get("")
async def list_sessions(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)) -> dict:
    with SessionLocal() as session:
        rows = session.execute(select(Conversation).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit)).scalars().all()
    return {"items": [{"id": row.id, "title": row.title, "owner": row.owner, "created_at": row.created_at.isoformat(), "updated_at": row.updated_at.isoformat()} for row in rows]}


@router.post("")
async def create_session(payload: SessionCreateRequest) -> dict:
    with SessionLocal() as session:
        item = Conversation(title=payload.title or "New conversation", owner=payload.owner)
        session.add(item)
        session.commit()
        session.refresh(item)
        return {"id": item.id, "title": item.title, "created_at": item.created_at.isoformat(), "updated_at": item.updated_at.isoformat()} 


@router.get("/{session_id}")
async def get_session(session_id: int) -> dict:
    with SessionLocal() as session:
        row = session.get(Conversation, session_id)
        if not row:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        return {"id": row.id, "title": row.title, "owner": row.owner, "created_at": row.created_at.isoformat(), "updated_at": row.updated_at.isoformat()}


@router.delete("/{session_id}")
async def delete_session(session_id: int) -> dict:
    with SessionLocal() as session:
        row = session.get(Conversation, session_id)
        if not row:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        session.delete(row)
        session.commit()
        return {"deleted": True, "session_id": session_id}


@router.get("/{session_id}/messages")
async def session_messages(session_id: int) -> dict:
    with SessionLocal() as session:
        conversation = session.get(Conversation, session_id)
        if not conversation:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        rows = session.execute(select(Message).where(Message.conversation_id == session_id).order_by(Message.timestamp.asc())).scalars().all()
        return {"session_id": session_id, "items": [{"id": row.id, "role": row.role, "content": row.content, "provider": row.provider, "model": row.model, "timestamp": row.timestamp.isoformat()} for row in rows]}
