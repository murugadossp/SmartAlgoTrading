"""Agent configuration: load and merge global agent defaults and per-agent config (instructions + config.yaml).
Config precedence: config/config.yaml (agents.default) then agents/<name>/config.yaml (per-agent wins).
"""
from pathlib import Path
from typing import Any

import yaml

# app/agents directory (sibling of app/config)
_APP_DIR = Path(__file__).resolve().parent.parent
AGENTS_DIR = _APP_DIR / "agents"


def get_global_agent_config() -> dict[str, Any]:
    """Load agent defaults from config/config.yaml → agents.default."""
    from app.config.settings import get_global_config
    cfg = get_global_config()
    return cfg.get("agents", {}).get("default", {})


def load_agent_config(agent_name: str, agents_dir: Path | None = None) -> tuple[str, dict[str, Any]]:
    """
    Load system instructions from .md and params from config.yaml for an agent.
    Returns (system_instructions_text, config_dict). Use for prompt templates (e.g. substitution).
    """
    base = agents_dir if agents_dir is not None else AGENTS_DIR
    agent_dir = base / agent_name
    if not agent_dir.is_dir():
        raise FileNotFoundError(f"Agent folder not found: {agent_dir}")
    md_path = agent_dir / "system_instructions.md"
    if not md_path.exists():
        raise FileNotFoundError(f"Agent system_instructions.md not found: {md_path}")
    system_instructions = md_path.read_text(encoding="utf-8")
    config_path = agent_dir / "config.yaml"
    config: dict[str, Any] = {}
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}
    return system_instructions, config


def get_effective_agent_config(
    agent_name: str,
    global_overrides: dict[str, Any] | None = None,
    agents_dir: Path | None = None,
) -> dict[str, Any]:
    """Merge global defaults, optional overrides, and per-agent config.yaml. Per-agent wins."""
    global_cfg = get_global_agent_config()
    _, agent_cfg = load_agent_config(agent_name, agents_dir=agents_dir)
    return {**global_cfg, **(global_overrides or {}), **agent_cfg}
