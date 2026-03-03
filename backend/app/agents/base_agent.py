"""BaseAgent: loads global config and per-agent .md + config.yaml; builds AGNO models and runs agents.
All agent and LLM logic lives inside BaseAgent (vendor-agnostic: OpenAI, Anthropic, etc.).

Usage:
  agent = BaseAgent("portfolio_parse_agent", output_schema=PortfolioParseResult)
  result = agent.run(user_message)

For one-off runs: BaseAgent.run_agent(agent_name, user_message, output_schema=..., **kwargs)
To load agent config (e.g. for prompt substitution): BaseAgent.load_agent_config(agent_name)

Config precedence: config/config.yaml (agents.default) then agents/<name>/config.yaml (per-agent wins).
"""
from pathlib import Path
from typing import Any, TypeVar

import yaml

T = TypeVar("T")


class BaseAgent:
    """
    Agent runner: holds agent name and options; all config loading and AGNO agent creation is inside the class.
    Invoke with .run(user_message); optional instructions_override can be passed to .run() for per-call prompts.
    """

    # Path to agents directory (sibling to this file)
    AGENTS_DIR = Path(__file__).resolve().parent

    def __init__(
        self,
        agent_name: str,
        *,
        output_schema: type[T] | None = None,
        instructions_override: str | None = None,
        **extra_agent_kwargs: Any,
    ):
        self.agent_name = agent_name
        self.output_schema = output_schema
        self.instructions_override = instructions_override
        self._extra = extra_agent_kwargs

    # ---------- Config loading (class method for use without an instance) ----------

    @classmethod
    def _load_global_config(cls) -> dict[str, Any]:
        """Load agent defaults from config/config.yaml → agents.default."""
        from app.config.settings import get_global_config
        cfg = get_global_config()
        return cfg.get("agents", {}).get("default", {})

    @classmethod
    def load_agent_config(cls, agent_name: str) -> tuple[str, dict[str, Any]]:
        """
        Load system instructions from .md and params from config.yaml for an agent.
        Returns (system_instructions_text, config_dict). Use when you need the prompt template (e.g. for substitution).
        """
        agent_dir = cls.AGENTS_DIR / agent_name
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

    def _get_effective_config(self, global_overrides: dict[str, Any] | None = None) -> dict[str, Any]:
        """Merge global defaults, optional overrides, and per-agent config.yaml. Per-agent wins."""
        global_cfg = self._load_global_config()
        _, agent_cfg = self.load_agent_config(self.agent_name)
        return {**global_cfg, **(global_overrides or {}), **agent_cfg}

    # ---------- AGNO model (Agent accepts "provider:model_id" and handles provider internally) ----------

    @classmethod
    def _get_agno_model_str(
        cls,
        provider: str | None = None,
        model_id: str | None = None,
    ) -> str:
        """
        Return AGNO model string "provider:model_id" (e.g. "openai:gpt-4o-mini").
        Agent class resolves provider and uses env API keys. Raises ValueError if API key is missing.
        """
        from app.config.settings import get_settings
        settings = get_settings()
        prov = (provider or getattr(settings, "llm_provider", "openai") or "openai").strip().lower()
        model = (model_id or getattr(settings, "llm_model", None) or "gpt-4o-mini").strip()
        # Fail fast if API key for this provider is not set
        if prov == "openai" and not (getattr(settings, "openai_api_key", None) or "").strip():
            raise ValueError("OpenAI provider requires OPENAI_API_KEY")
        if prov == "anthropic" and not (getattr(settings, "anthropic_api_key", None) or "").strip():
            raise ValueError("Anthropic provider requires ANTHROPIC_API_KEY")
        return f"{prov}:{model}"

    def _get_agno_agent(self, instructions_override: str | None = None) -> Any:
        """
        Build and return AGNO Agent for this agent name with current options.
        Returns None if config/model unavailable (e.g. missing API key).
        """
        try:
            system_instructions, _ = self.load_agent_config(self.agent_name)
        except FileNotFoundError:
            return None
        instructions = instructions_override if instructions_override is not None else (
            self.instructions_override if self.instructions_override is not None else system_instructions
        )
        effective = self._get_effective_config()
        try:
            model_str = self._get_agno_model_str(
                provider=effective.get("provider"),
                model_id=effective.get("model"),
            )
        except ValueError:
            return None
        from agno.agent import Agent
        temperature = float(effective.get("temperature", 0.2))
        max_tokens = int(effective.get("max_tokens", 1024))
        kwargs: dict[str, Any] = {
            "model": model_str,
            "instructions": instructions,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **self._extra,
        }
        if self.output_schema is not None:
            kwargs["output_schema"] = self.output_schema
        return Agent(**kwargs)

    def run(
        self,
        user_message: str,
        *,
        instructions_override: str | None = None,
    ) -> str | T | None:
        """
        Run the agent with the given user message; return content (str or output_schema instance) or None.
        instructions_override: optional per-call override (e.g. substituted prompt); wins over constructor value.
        """
        agent = self._get_agno_agent(instructions_override=instructions_override)
        if agent is None:
            return None
        try:
            response = agent.run(user_message)
            if not response or not hasattr(response, "content"):
                return None
            content = response.content
            if self.output_schema is not None and isinstance(content, self.output_schema):
                return content
            if content is None:
                return None
            return content if isinstance(content, str) else str(content)
        except Exception:
            return None

    # ---------- Class methods for one-off use (no need to hold an instance) ----------

    @classmethod
    def get_agno_agent(
        cls,
        agent_name: str,
        *,
        output_schema: type[T] | None = None,
        instructions_override: str | None = None,
        **extra_agent_kwargs: Any,
    ) -> Any:
        """
        Build and return an AGNO Agent for the given agent_name and options.
        Returns None if config/model unavailable.
        """
        instance = cls(agent_name, output_schema=output_schema, instructions_override=instructions_override, **extra_agent_kwargs)
        return instance._get_agno_agent(instructions_override=instructions_override)

    @classmethod
    def run_agent(
        cls,
        agent_name: str,
        user_message: str,
        *,
        output_schema: type[T] | None = None,
        instructions_override: str | None = None,
        **extra_agent_kwargs: Any,
    ) -> str | T | None:
        """
        One-off run: get agent for agent_name, run with user_message, return content.
        If output_schema is set, returns validated Pydantic instance or None; otherwise response string or None.
        """
        instance = cls(agent_name, output_schema=output_schema, instructions_override=instructions_override, **extra_agent_kwargs)
        return instance.run(user_message, instructions_override=instructions_override)
