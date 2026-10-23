from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    """Runtime configuration. Every value has a safe local default."""

    def __init__(self) -> None:
        self.base_dir = BASE_DIR
        self.storage_dir = Path(os.getenv("PRISMCHECK_STORAGE", BASE_DIR / "storage"))
        self.db_path = Path(os.getenv("PRISMCHECK_DB", BASE_DIR / "prismcheck.db"))
        self.secret_key = os.getenv("PRISMCHECK_SECRET", "dev-only-change-me")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "").strip()
        self.model_mode = os.getenv("PRISMCHECK_MODEL", "auto").strip().lower()
        self.max_upload_mb = int(os.getenv("PRISMCHECK_MAX_UPLOAD_MB", "8"))
        self.cookie_secure = _bool(os.getenv("PRISMCHECK_COOKIE_SECURE"), False)
        self.demo_mode = _bool(os.getenv("PRISMCHECK_DEMO_MODE"), True)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.db_path.as_posix()}"


settings = Settings()
