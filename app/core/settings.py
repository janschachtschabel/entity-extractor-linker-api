"""Central configuration using environment variables.

Uses Pydantic BaseSettings so values can be provided via env vars or a local
`.env` file. All modules should import *settings* instead of reading os.getenv
manually. This avoids scattered config logic.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import ConfigDict, Field, ValidationError  # type: ignore
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    """Project-wide settings (loaded once at import time)."""

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = Field("entityextractorbatch", description="Project name for user agent and logging")
    VERSION: str = Field("0.1.0", description="Project version for user agent and logging")

    # OpenAI
    OPENAI_API_KEY: str = Field("", description="API key for openai package")
    OPENAI_MODEL: str = Field(
        "gpt-4o-mini",
        description="Default model name used for ChatCompletion calls.",
    )
    OPENAI_TIMEOUT: int = Field(120, ge=10, description="Timeout for OpenAI requests (seconds)")

    # Wikipedia
    WIKIPEDIA_TIMEOUT: int = Field(30, ge=1, description="HTTP timeout for Wikipedia API requests (seconds)")
    WIKIPEDIA_MAX_CONCURRENCY: int = Field(5, ge=1, description="Max simultaneous Wikipedia requests")
    WIKIPEDIA_BATCH_SIZE: int = Field(10, ge=1, description="Number of entities to process in a batch")

    # Cache
    CACHE_DIR: str = Field("./cache", description="Directory for caching service responses")

    # Rate limiting
    RATE_LIMIT: int = Field(60, ge=1, description="Max requests per minute per IP")
    RATE_WINDOW: int = Field(60, ge=10, description="Rate limit window in seconds")

    # Text splitter
    TEXT_SPLIT_THRESHOLD: int = Field(4000, ge=500, description="Chars above which the linker auto-splits the text")
    TEXT_CHUNK_SIZE: int = Field(800, ge=200, description="Chunk size for utils.split_text")


@lru_cache(maxsize=1)
def get_settings() -> _Settings:  # pragma: no cover – trivial
    """Return a cached instance of settings (cheap to keep)."""
    try:
        return _Settings()  # type: ignore[call-arg]
    except ValidationError as exc:  # pragma: no cover – misconfigured env
        raise RuntimeError(f"Invalid environment configuration: {exc}") from exc


# Eagerly evaluate for convenience import style: `from .settings import settings`
settings = get_settings()

__all__: list[str] = ["get_settings", "settings"]
