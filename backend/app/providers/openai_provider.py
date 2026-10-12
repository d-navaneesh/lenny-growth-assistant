from __future__ import annotations

import os

from openai import OpenAI

from app.core.config import get_settings
from app.providers.base import BaseProvider, ProviderStatus

settings = get_settings()


class OpenAIProvider(BaseProvider):
    name = "openai"

    async def status(self, model: str | None = None) -> ProviderStatus:
        if not settings.openai_api_key:
            return ProviderStatus(name="openai", available=False, model=model or "gpt-4o-mini", error="Missing OPENAI_API_KEY")
        return ProviderStatus(name="openai", available=True, model=model or "gpt-4o-mini")

    async def generate(self, prompt: str, model: str | None = None, **kwargs) -> str:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.responses.create(
            model=model or "gpt-4o-mini",
            input=prompt,
            temperature=0.2,
        )
        return response.output_text.strip() or "No response from OpenAI."
