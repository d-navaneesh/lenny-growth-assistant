from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Lenny Growth Assistant"
    api_v1_str: str = "/api/v1"
    environment: str = "development"
    log_level: str = "INFO"

    database_url: str = Field(
        default="sqlite:///./lenny.db",
        alias="DATABASE_URL",
    )
    test_database_url: str = Field(
        default="sqlite+pysqlite:///./test.db",
        alias="TEST_DATABASE_URL",
    )

    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.2:3b", alias="OLLAMA_MODEL")
    default_provider: Literal["ollama", "openai", "anthropic"] = Field(
        default="ollama",
        alias="DEFAULT_PROVIDER",
    )
    selected_provider: Literal["ollama", "openai", "anthropic"] = Field(
        default="ollama",
        alias="SELECTED_PROVIDER",
    )
    selected_model: str = Field(default="llama3.2:3b", alias="SELECTED_MODEL")

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")

    max_chunk_chars: int = 900
    chunk_overlap: int = 120
    retrieval_top_k: int = 4

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
