import os

from pydantic_settings import BaseSettings


def _default_ollama_base_url() -> str:
    if os.path.exists("/.dockerenv"):
        return "http://ollama:11434"
    return "http://localhost:11434"


class Settings(BaseSettings):

    app_name: str = "Chatbot Fact Checker"
    upload_dir: str = "data/uploads"
    system_files_dir: str = "data/system_files"
    max_upload_mb: int = 10
    redis_url: str | None = "redis://redis:6379/0"
    ollama_base_url: str = _default_ollama_base_url()
    ollama_model: str = "smollm2:135m-instruct-q4_1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
