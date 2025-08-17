from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Super Agent"
    app_env: str = "development"
    admin_api_key: Optional[str] = None

    # CORS
    allowed_origins: List[str] = ["*"]

    # AI providers
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    google_cx: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    ollama_host: str = "http://127.0.0.1:11434"
    default_ai_provider: Optional[str] = None

    # Plugins
    plugin_autoload: bool = True
    plugin_dirs: List[str] = [
        "backend/app/plugins",
        "app/plugins",
    ]

    # Security
    enable_sandbox: bool = True

    # Networking
    http_timeout_seconds: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    s = Settings()
    # normalize allowed_origins if provided as comma-separated env
    if isinstance(s.allowed_origins, list) and len(s.allowed_origins) == 1 and "," in s.allowed_origins[0]:
        s.allowed_origins = [x.strip() for x in s.allowed_origins[0].split(",") if x.strip()]
    return s