from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.db.models import Artifact, Conversation
from app.db.session import SessionLocal

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


class ArtifactCreateRequest(BaseModel):
    conversation_id: int | None = None
    title: str = Field(..., min_length=1, max_length=255)
    artifact_type: str = Field(default="markdown")
    content: str = Field(..., min_length=1, max_length=200000)


@router.post("")
async def create_artifact(payload: ArtifactCreateRequest) -> dict:
    with SessionLocal() as session:
        if payload.conversation_id is not None:
            conversation = session.get(Conversation, payload.conversation_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = None
        artifact = Artifact(
            conversation_id=payload.conversation_id,
            title=payload.title,
            artifact_type=payload.artifact_type,
            content=payload.content,
            validation_status="valid",
            rendering_metadata={"sandbox": "restrictive", "preview": "iframe"},
        )
        session.add(artifact)
        session.commit()
        session.refresh(artifact)
        return {"id": artifact.id, "title": artifact.title, "type": artifact.artifact_type, "created_at": artifact.created_at.isoformat(), "conversation_id": artifact.conversation_id}


@router.get("/{artifact_id}")
async def get_artifact(artifact_id: int) -> dict:
    with SessionLocal() as session:
        artifact = session.get(Artifact, artifact_id)
        if not artifact:
            raise HTTPException(status_code=404, detail="Artifact not found")
        return {"id": artifact.id, "title": artifact.title, "type": artifact.artifact_type, "content": artifact.content, "created_at": artifact.created_at.isoformat(), "validation_status": artifact.validation_status}
