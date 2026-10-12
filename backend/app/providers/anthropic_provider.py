from __future__ import annotations

from anthropic import Anthropic

from app.core.config import get_settings
from app.providers.base import BaseProvider, ProviderStatus

settings = get_settings()


class AnthropicProvider(BaseProvider):
    name = "anthropic"

    async def status(self, model: str | None = None) -> ProviderStatus:
        if not settings.anthropic_api_key:
            return ProviderStatus(name="anthropic", available=False, model=model or "claude-3-5-sonnet-20241022", error="Missing ANTHROPIC_API_KEY")
        return ProviderStatus(name="anthropic", available=True, model=model or "claude-3-5-sonnet-20241022")

    async def generate(self, prompt: str, model: str | None = None, **kwargs) -> str:
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not configured.")
        client = Anthropic(api_key=settings.anthropic_api_key)
        message = client.messages.create(
            model=model or "claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
