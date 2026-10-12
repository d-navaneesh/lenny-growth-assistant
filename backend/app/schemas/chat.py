from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"] = "user"
    content: str = Field(..., min_length=1, max_length=20000)


class ChatRequest(BaseModel):
    session_id: int | None = None
    prompt: str = Field(..., min_length=1, max_length=3000)
    provider: Literal["ollama", "openai", "anthropic"] | None = None
    model: str | None = None
    mode: str = "grounded"


class EvidenceItem(BaseModel):
    source_title: str
    excerpt: str
    score: float | None = None
    url: str | None = None
    chunk_id: int | None = None


class ChatResponse(BaseModel):
    response: str
    provider: str
    model: str
    mode: str
    evidence: list[EvidenceItem] = []
    trace_id: str
    source_supported: bool = True
