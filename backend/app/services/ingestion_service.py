from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from sqlalchemy import select

from app.db.models import TranscriptChunk, TranscriptSource
from app.db.session import SessionLocal

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT_PATH = ROOT / "data" / "transcripts" / "sample_transcripts.json"


def chunk_text(text: str, max_chars: int = 900, overlap: int = 120) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == len(text):
            break
        start = max(start + max_chars - overlap, end - overlap)
    return chunks


def ingest_transcripts() -> dict:
    if not TRANSCRIPT_PATH.exists():
        return {"status": "skipped", "sources": 0, "chunks": 0, "message": "No transcript fixtures found."}

    with TRANSCRIPT_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    inserted = 0
    chunks_total = 0
    with SessionLocal() as session:
        for source in payload.get("sources", []):
            content = "\n\n".join(chunk["text"] for chunk in source.get("chunks", []))
            digest = sha256(content.encode("utf-8")).hexdigest()
            existing = session.execute(select(TranscriptSource).where(TranscriptSource.content_hash == digest)).scalar_one_or_none()
            if existing:
                continue
            source_record = TranscriptSource(
                title=source["title"],
                source_url=source.get("url"),
                author=source.get("author"),
                episode=source.get("episode"),
                content_hash=digest,
                status="indexed",
                source_metadata={"synthetic_demo": True}
            )
            session.add(source_record)
            session.flush()
            chunks = chunk_text(content)
            for index, chunk_text in enumerate(chunks):
                session.add(TranscriptChunk(
                    source_id=source_record.id,
                    chunk_index=index,
                    chunk_text=chunk_text,
                    char_count=len(chunk_text),
                    metadata={"source_title": source["title"]},
                ))
                chunks_total += 1
            inserted += 1
        session.commit()
    return {"status": "ok", "sources": inserted, "chunks": chunks_total}
