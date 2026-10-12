from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProviderStatus:
    name: str
    available: bool
    model: str
    error: str | None = None


class BaseProvider:
    name: str = "base"

    async def generate(self, prompt: str, model: str | None = None, **kwargs) -> str:
        raise NotImplementedError

    async def status(self, model: str | None = None) -> ProviderStatus:
        raise NotImplementedError
