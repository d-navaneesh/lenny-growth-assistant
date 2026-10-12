from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.core.config import get_settings
from app.db.models import Conversation, Message
from app.db.session import SessionLocal
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.openai_provider import OpenAIProvider
from app.retrieval.service import search_transcripts
from app.schemas.chat import ChatRequest, EvidenceItem

router = APIRouter(prefix="/chat", tags=["chat"])
settings = get_settings()


def get_provider():
    providers = {
        "ollama": OllamaProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
    }
    provider_class = providers.get(settings.selected_provider)
    if provider_class is None:
        raise RuntimeError(f"Unsupported provider: {settings.selected_provider}")
    return provider_class()


@router.post("")
async def chat(payload: ChatRequest) -> dict:
    with SessionLocal() as session:
        conversation = None
        if payload.session_id is not None:
            conversation = session.get(Conversation, payload.session_id)

        if conversation is None:
            conversation = Conversation(
                title=(payload.prompt[:40] or "New conversation"),
                owner="local-demo",
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=payload.prompt,
            message_metadata={"mode": payload.mode},
        )
        session.add(user_message)
        session.commit()

        evidence = search_transcripts(
            payload.prompt,
            top_k=settings.retrieval_top_k,
        )

        evidence_entries = [
            EvidenceItem(
                source_title=item["source_title"],
                excerpt=item["excerpt"],
                score=item.get("score"),
                url=item.get("url"),
                chunk_id=item.get("chunk_id"),
            )
            for item in evidence
        ]

        if not evidence:
            response_text = (
                "I couldn't find relevant passages in the currently indexed "
                "sources, so I can't provide a source-grounded answer. "
                "Try a narrower question or ingest more relevant material."
            )
            source_supported = False
        else:
            context = "\n\n".join(
                f"[Source {index}]\n"
                f"Title: {item['source_title']}\n"
                f"URL: {item.get('url') or 'URL not available'}\n"
                f"Passage: {item['excerpt']}"
                for index, item in enumerate(evidence, start=1)
            )

            generation_prompt = f"""You are Lenny Growth Assistant, a research assistant for startup founders.

Answer the user's latest question directly and use the source passages below as your evidence.

Rules:
- Treat the passages as the only source of factual claims about what the sources say.
- Cite supported claims inline using [Source 1], [Source 2], etc.
- Never invent quotations, source titles, URLs, or citations.
- Distinguish source-supported findings from your own recommendations.
- Explicitly say when the supplied passages do not establish a claim.
- For a request for steps, give numbered, actionable steps with reasoning.
- For a request for a Ship 30 for 30 essay, write an essay rather than a list of excerpts. Follow the requested length and structure as closely as possible, while keeping source claims grounded.
- If asked a follow-up, answer that question directly; do not merely repeat the evidence list.

Retrieved passages:
{context}

User question:
{payload.prompt}
"""

            try:
                provider = get_provider()
                response_text = await provider.generate(
                    generation_prompt,
                    model=settings.selected_model,
                )
                if not response_text.strip():
                    raise RuntimeError("The selected provider returned an empty response.")
                source_supported = True
            except Exception as exc:
                raise HTTPException(
                    status_code=502,
                    detail=(
                        f"Text generation failed using "
                        f"{settings.selected_provider}: {exc}"
                    ),
                ) from exc

        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response_text,
            provider=settings.selected_provider,
            model=settings.selected_model,
            message_metadata={
                "evidence": [item.model_dump() for item in evidence_entries]
            },
        )
        session.add(assistant_message)
        session.commit()

        conversation.updated_at = datetime.now(timezone.utc)
        session.commit()

        return {
            "response": response_text,
            "provider": settings.selected_provider,
            "model": settings.selected_model,
            "mode": payload.mode,
            "evidence": [item.model_dump() for item in evidence_entries],
            "trace_id": f"trace-{conversation.id}-{assistant_message.id}",
            "source_supported": source_supported,
        }