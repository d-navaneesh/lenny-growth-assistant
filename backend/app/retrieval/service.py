from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TRANSCRIPT_PATH = ROOT / "data" / "transcripts" / "sample_transcripts.json"


def _normalize_tokens(value: str) -> list[str]:
    return [token for token in re.split(r"[^a-z0-9]+", (value or "").lower()) if token]


def _read_fixture_data() -> list[dict]:
    if not TRANSCRIPT_PATH.exists():
        return []
    with TRANSCRIPT_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload.get("sources", [])


def search_transcripts(query: str, top_k: int = 4) -> list[dict]:
    query_tokens = _normalize_tokens(query)
    if not query_tokens:
        return []

    results: list[dict] = []
    for source in _read_fixture_data():
        for i, chunk in enumerate(source.get("chunks", [])):
            content = chunk["text"].lower()
            content_tokens = _normalize_tokens(content)
            score = 0
            for token in query_tokens:
                if token in content_tokens:
                    score += 2
                if token in content:
                    score += 1
            if score > 0:
                results.append({
                    "source_title": source["title"],
                    "url": source.get("url"),
                    "excerpt": chunk["text"],
                    "score": float(round(score / max(1, len(query_tokens)), 2)),
                    "chunk_id": i,
                })
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


def get_all_sources() -> list[dict]:
    return _read_fixture_data()
