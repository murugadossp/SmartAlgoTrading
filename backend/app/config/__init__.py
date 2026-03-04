"""Config module: global app settings, config (broker, llm, agents.default), and agent config loading."""
from app.config.settings import get_global_config, get_settings

__all__ = ["get_settings", "get_global_config"]

# Agent config (load + merge per-agent): use agent_config.load_agent_config, get_effective_agent_config, get_global_agent_config
