from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.openai_provider import OpenAIProvider

router = APIRouter(prefix="/models", tags=["models"])
settings = get_settings()


class ModelSelectionRequest(BaseModel):
    provider: str = Field(..., pattern="^(ollama|openai|anthropic)$")
    model: str | None = None


async def provider_status_summary() -> list[dict]:
    providers = {
        "ollama": OllamaProvider(),
        "openai": OpenAIProvider(),
        "anthropic": AnthropicProvider(),
    }
    result = []
    for name, provider in providers.items():
        status = await provider.status(provider_name := settings.ollama_model if name == "ollama" else None)
        result.append({
            "provider": name,
            "available": status.available,
            "model": status.model,
            "error": status.error,
        })
    return result


@router.get("")
async def list_models() -> dict:
    return {"models": await provider_status_summary()}


@router.get("/status")
async def model_status() -> dict:
    return {"providers": await provider_status_summary(), "selected_provider": settings.selected_provider, "selected_model": settings.selected_model}


@router.post("/select")
async def select_model(payload: ModelSelectionRequest) -> dict:
    if payload.provider not in {"ollama", "openai", "anthropic"}:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    settings.selected_provider = payload.provider
    settings.selected_model = payload.model or (settings.ollama_model if payload.provider == "ollama" else "gpt-4o-mini" if payload.provider == "openai" else "claude-3-5-sonnet-20241022")
    return {"provider": settings.selected_provider, "model": settings.selected_model}
