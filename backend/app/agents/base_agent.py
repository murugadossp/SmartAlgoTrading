"""BaseAgent: loads global config and per-agent .md + config.yaml; applies overrides.
Model calls use app.agents.llm_factory (AGNO, vendor-agnostic). This module handles config loading and prompt construction.
"""
from pathlib import Path
from typing import Any

import yaml

# Path to agents directory (sibling to this file)
AGENTS_DIR = Path(__file__).resolve().parent


def load_global_agent_config() -> dict[str, Any]:
    """Load global agent defaults from config module (e.g. global_agent_config.yaml)."""
    config_dir = Path(__file__).resolve().parent.parent / "config"
    global_path = config_dir / "global_agent_config.yaml"
    if not global_path.exists():
        return {}
    with open(global_path) as f:
        data = yaml.safe_load(f) or {}
    return data.get("default", data)


def load_agent_config(agent_name: str) -> tuple[str, dict[str, Any]]:
    """Load system instructions from .md and params from config.yaml for an agent.
    Returns (system_instructions_text, config_dict). Config dict has model, temperature, etc. (no prompt text).
    """
    agent_dir = AGENTS_DIR / agent_name
    if not agent_dir.is_dir():
        raise FileNotFoundError(f"Agent folder not found: {agent_dir}")

    # Prompts from .md
    md_path = agent_dir / "system_instructions.md"
    if not md_path.exists():
        raise FileNotFoundError(f"Agent system_instructions.md not found: {md_path}")
    system_instructions = md_path.read_text(encoding="utf-8")

    # Other info from config.yaml
    config_path = agent_dir / "config.yaml"
    config: dict[str, Any] = {}
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}

    return system_instructions, config


def get_effective_agent_config(agent_name: str, global_overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    """Merge global defaults, optional central overrides, and per-agent config.yaml. Per-agent wins."""
    global_cfg = load_global_agent_config()
    _, agent_cfg = load_agent_config(agent_name)
    merged = {**global_cfg, **(global_overrides or {}), **agent_cfg}
    return merged
