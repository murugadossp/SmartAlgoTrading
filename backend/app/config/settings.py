"""Global app settings from environment."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    api_title: str = "Smart Algo Trading API"
    api_version: str = "0.1.0"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    dhan_access_token: str = ""
    dhan_client_id: str = ""
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    serper_api_key: str = ""
    config_path: str = ""


def get_settings() -> Settings:
    return Settings()
