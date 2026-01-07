from functools import lru_cache
import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_ollama_base_url() -> str:
    if os.path.exists("/.dockerenv"):
        return "http://ollama:11434"
    return "http://localhost:11434"


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(...,alias="APP_NAME")
    upload_dir: str = Field(...,alias="UPLOAD_DIR")
    system_files_dir: str = Field(...,alias="SYSTEM_FILES_DIR")
    max_upload_mb: int = Field(...,alias="MAX_UPLOAD_MB")
    redis_url: str = Field(...,alias="REDIS_URL")
    ollama_base_url: str = Field(default_factory=_default_ollama_base_url)
    ollama_model: str = Field(...,alias="OLLAMA_MODEL")
    database_url: str = Field(...,alias="DATABASE_URL")
    minio_endpoint: str | None = None
    minio_access_key: str | None = None
    minio_secret_key: str | None = None
    minio_bucket: str | None = None
    minio_secure: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore[call-arg]

settings = get_settings()