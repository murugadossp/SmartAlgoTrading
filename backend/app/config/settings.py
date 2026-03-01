"""Global app settings: env for secrets, config.yaml for non-secret broker/app options."""
import os
from pathlib import Path

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    api_title: str = "Smart Algo Trading API"
    api_version: str = "0.1.0"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    broker_provider: str = "dhan"
    dhan_access_token: str = ""
    dhan_client_id: str = ""
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    serper_api_key: str = ""
    config_path: str = ""


def _load_global_config() -> dict:
    """Load config.yaml (non-secret broker/app options). Secrets stay in env."""
    base = Path(__file__).resolve().parent.parent.parent
    config_path = os.environ.get("CONFIG_PATH", "").strip()
    if config_path:
        path = Path(config_path)
        if path.is_dir():
            path = path / "config.yaml"
    else:
        path = base / "config" / "config.yaml"
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def get_settings() -> Settings:
    s = Settings()
    cfg = _load_global_config()
    if cfg.get("broker", {}).get("provider"):
        s.broker_provider = (cfg["broker"].get("provider") or s.broker_provider).strip().lower()
    return s
