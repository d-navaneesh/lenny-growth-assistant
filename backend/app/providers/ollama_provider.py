from __future__ import annotations

import json

import httpx

from app.core.config import get_settings
from app.providers.base import BaseProvider, ProviderStatus

settings = get_settings()


class OllamaProvider(BaseProvider):
    name = "ollama"

    async def status(self, model: str | None = None) -> ProviderStatus:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{settings.ollama_base_url}/api/tags")
                response.raise_for_status()
            return ProviderStatus(name="ollama", available=True, model=model or settings.ollama_model)
        except Exception as exc:
            return ProviderStatus(name="ollama", available=False, model=model or settings.ollama_model, error=str(exc))

    async def generate(self, prompt: str, model: str | None = None, **kwargs) -> str:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {"model": model or settings.ollama_model, "prompt": prompt, "stream": False}
                response = await client.post(f"{settings.ollama_base_url}/api/generate", json=payload)
                response.raise_for_status()
                payload = response.json()
                return payload.get("response", "No response from Ollama.")
        except Exception as exc:
            raise RuntimeError(f"Ollama is unavailable: {exc}") from exc
