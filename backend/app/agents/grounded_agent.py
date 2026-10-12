from __future__ import annotations

from app.core.config import get_settings
from app.retrieval.service import search_transcripts

settings = get_settings()


class GroundedAgent:
    def __init__(self):
        self.provider = settings.selected_provider

    def execute(self, prompt: str, mode: str = "grounded") -> dict:
        evidence = search_transcripts(prompt, top_k=settings.retrieval_top_k)
        if not evidence:
            return {
                "response": "I do not have enough transcript-grounded evidence to answer that confidently. Please ask a narrower product or growth question with clearer context.",
                "evidence": [],
                "provider": settings.selected_provider,
                "model": settings.selected_model,
                "mode": mode,
            }

        context = "\n\n".join(f"- {item['source_title']}: {item['excerpt']}" for item in evidence)
        response = (
            "Here is a grounded recommendation based on the evidence in the transcript material:\n\n"
            f"{context}\n\n"
            "The key pattern is that durable product growth comes from a noisy but repeated cycle of learning, segmented validation, and disciplined iteration."
        )
        return {
            "response": response,
            "evidence": evidence,
            "provider": settings.selected_provider,
            "model": settings.selected_model,
            "mode": mode,
        }
