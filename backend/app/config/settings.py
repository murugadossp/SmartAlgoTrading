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
    # LLM: populated from config (agents.default) in get_settings(); do not set in .env
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
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


def get_global_config() -> dict:
    """Return the full app config dict from config/config.yaml (same file as used by get_settings)."""
    return _load_global_config()


def get_settings() -> Settings:
    s = Settings()
    cfg = _load_global_config()
    if cfg.get("broker", {}).get("provider"):
        s.broker_provider = (cfg["broker"].get("provider") or s.broker_provider).strip().lower()
    agents_default = cfg.get("agents", {}).get("default") or {}
    if agents_default.get("provider"):
        s.llm_provider = (agents_default.get("provider") or s.llm_provider).strip().lower()
    if agents_default.get("model"):
        s.llm_model = (agents_default.get("model") or s.llm_model).strip()
    return s
