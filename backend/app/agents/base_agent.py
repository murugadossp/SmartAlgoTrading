"""BaseAgent: builds AGNO models and runs agents. Config loading is in app.config.agent_config.

Usage:
  agent = BaseAgent("portfolio_parse_agent", output_schema=PortfolioParseResult)
  result = agent.run(user_message)

One-off run: BaseAgent(agent_name, output_schema=...).run(user_message)
To load agent config (e.g. for prompt substitution): BaseAgent.load_agent_config(agent_name) or agent_config.load_agent_config(agent_name)
"""
from typing import Any, TypeVar

from app.config import agent_config
from app.logger import append_agent_trace, get_logger, trace_timestamp

T = TypeVar("T")
logger = get_logger(__name__)


class BaseAgent:
    """
    Agent runner: holds agent name and options; uses agent_config for config, builds AGNO model and runs.
    Invoke with .run(user_message); optional instructions_override can be passed to .run() for per-call prompts.
    """

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

    # ---------- Config: delegate to app.config.agent_config ----------

    @classmethod
    def load_agent_config(cls, agent_name: str) -> tuple[str, dict[str, Any]]:
        """
        Load system instructions and config for an agent. Delegates to agent_config.load_agent_config.
        Returns (system_instructions_text, config_dict). Use for prompt template (e.g. substitution).
        """
        return agent_config.load_agent_config(agent_name)

    # ---------- AGNO model: instantiate provider-specific model class, then Agent(model=...) ----------

    @classmethod
    def _get_agno_model(
        cls,
        provider: str | None = None,
        model_id: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> Any:
        """
        Return an AGNO model instance for the given provider (e.g. OpenAIResponses, Claude).
        Agent is then used as Agent(model=model, instructions=..., ...). Raises ValueError if unsupported or API key missing.
        """
        from app.config.settings import get_settings
        settings = get_settings()
        prov = (provider or getattr(settings, "llm_provider", "openai") or "openai").strip().lower()
        model = (model_id or getattr(settings, "llm_model", None) or "gpt-4o-mini").strip()

        logger.info(
            "model params: provider=%s model_id=%s temperature=%s max_tokens=%s",
            prov, model, temperature, max_tokens,
        )

        if prov == "openai":
            key = (getattr(settings, "openai_api_key", None) or "").strip()
            if not key:
                raise ValueError("OpenAI provider requires OPENAI_API_KEY")
            from agno.models.openai import OpenAIResponses
            # Some OpenAI models (e.g. o1, o3, gpt-5-mini) do not support temperature
            supports_temperature = not any(
                x in model.lower() for x in ("o1", "o3", "gpt-5-mini")
            )
            kwargs: dict[str, Any] = {"id": model, "api_key": key}
            if temperature is not None and supports_temperature:
                kwargs["temperature"] = temperature
            if max_tokens is not None:
                kwargs["max_output_tokens"] = max_tokens
            return OpenAIResponses(**kwargs)

        if prov == "anthropic":
            key = (getattr(settings, "anthropic_api_key", None) or "").strip()
            if not key:
                raise ValueError("Anthropic provider requires ANTHROPIC_API_KEY")
            from agno.models.anthropic import Claude
            kwargs = {"id": model, "api_key": key}
            if temperature is not None:
                kwargs["temperature"] = temperature
            if max_tokens is not None:
                kwargs["max_tokens"] = max_tokens
            return Claude(**kwargs)

        raise ValueError(f"Unsupported LLM provider: {prov}. Use openai or anthropic.")

    def _get_agno_agent(self, instructions_override: str | None = None) -> Any:
        """
        Build and return AGNO Agent for this agent name with current options.
        Uses provider-specific model instance (e.g. OpenAIResponses(id="gpt-4o-mini")) then Agent(model=model, ...).
        """
        try:
            system_instructions, _ = agent_config.load_agent_config(self.agent_name)
        except FileNotFoundError:
            return None
        instructions = instructions_override if instructions_override is not None else (
            self.instructions_override if self.instructions_override is not None else system_instructions
        )
        effective = agent_config.get_effective_agent_config(self.agent_name)
        provider = effective.get("provider")
        model_id = effective.get("model")
        temperature = float(effective.get("temperature", 0.2))
        max_tokens = int(effective.get("max_tokens", 1024))
        logger.info(
            "agent build: agent_name=%s provider=%s model_id=%s temperature=%s max_tokens=%s output_schema=%s",
            self.agent_name, provider, model_id, temperature, max_tokens,
            getattr(self.output_schema, "__name__", str(self.output_schema)) if self.output_schema else None,
        )
        try:
            model = self._get_agno_model(
                provider=provider,
                model_id=model_id,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except ValueError as e:
            logger.warning("agent build failed (config/model): agent_name=%s error=%s", self.agent_name, e)
            return None
        from agno.agent import Agent
        kwargs: dict[str, Any] = {"model": model, "instructions": instructions, **self._extra}
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
        Each run is logged as one JSON line in backend/logs/agent_traces.json (timestamp, agent_name, model_config, input, output).
        """
        start_time = trace_timestamp()
        user_message = user_message or ""
        system_instructions = ""
        model_config: dict[str, Any] = {}
        try:
            system_instructions, _ = agent_config.load_agent_config(self.agent_name)
            effective = agent_config.get_effective_agent_config(self.agent_name)
            model_config = {
                k: effective.get(k)
                for k in ("provider", "model", "temperature", "max_tokens")
            }
        except FileNotFoundError:
            pass
        instructions = (
            instructions_override
            if instructions_override is not None
            else (self.instructions_override if self.instructions_override is not None else system_instructions)
        )
        trace_input = {"system_instructions": instructions, "user_message": user_message}

        def _write_trace(output: Any) -> None:
            payload = {
                "timestamp": start_time,
                "agent_name": self.agent_name,
                "model_config": model_config,
                "input": trace_input,
                "output": output,
            }
            append_agent_trace(payload)

        logger.info("run start: agent_name=%s user_message_len=%s", self.agent_name, len(user_message))
        agent = self._get_agno_agent(instructions_override=instructions_override)
        if agent is None:
            logger.warning("run skipped: agent_name=%s (agent build returned None)", self.agent_name)
            _write_trace({"error": "agent build returned None"})
            return None
        try:
            response = agent.run(user_message)
            if not response or not hasattr(response, "content"):
                logger.warning("run empty response: agent_name=%s", self.agent_name)
                _write_trace({"error": "empty response"})
                return None
            content = response.content
            if content is None:
                logger.warning("run None content: agent_name=%s", self.agent_name)
                _write_trace(None)
                return None
            # Serialize output for trace (Pydantic model -> dict, else string; logger uses default=str for JSON)
            if hasattr(content, "model_dump"):
                out_val: Any = content.model_dump()
            else:
                out_val = str(content) if content is not None else None
            _write_trace(out_val)
            if self.output_schema is not None and isinstance(content, self.output_schema):
                logger.info("run success: agent_name=%s result_type=%s", self.agent_name, type(content).__name__)
                return content
            logger.info("run success: agent_name=%s result_type=str", self.agent_name)
            return content if isinstance(content, str) else str(content)
        except Exception as e:
            logger.exception("run failed: agent_name=%s error=%s", self.agent_name, e)
            _write_trace({"error": str(e)})
            return None

    # ---------- Class method for getting raw AGNO Agent (e.g. for debugging) ----------

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
        Returns None if config/model unavailable. For running, use BaseAgent(agent_name, ...).run(user_message).
        """
        instance = cls(agent_name, output_schema=output_schema, instructions_override=instructions_override, **extra_agent_kwargs)
        return instance._get_agno_agent(instructions_override=instructions_override)
