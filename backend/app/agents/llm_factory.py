"""Vendor-agnostic LLM factory using AGNO. Builds Agno model instances and runs agents."""
from __future__ import annotations

from typing import Any

from app.config.settings import get_settings


def get_agno_model(
    provider: str | None = None,
    model_id: str | None = None,
    api_key: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> Any:
    """
    Return an AGNO model instance for the given provider (openai, anthropic, etc.).
    Uses settings for provider/model/keys when not passed. Raises ValueError if
    provider is unsupported or API key is missing for the chosen provider.
    """
    settings = get_settings()
    prov = (provider or getattr(settings, "llm_provider", "openai") or "openai").strip().lower()
    model = model_id or getattr(settings, "llm_model", None) or "gpt-4o-mini"

    if prov == "openai":
        key = api_key or settings.openai_api_key
        if not key:
            raise ValueError("OpenAI provider requires OPENAI_API_KEY")
        from agno.models.openai import OpenAIChat

        kwargs = {"id": model, "api_key": key}
        if temperature is not None:
            kwargs["temperature"] = temperature
        if max_tokens is not None:
            kwargs["max_completion_tokens"] = max_tokens
        return OpenAIChat(**kwargs)

    if prov == "anthropic":
        key = api_key or getattr(settings, "anthropic_api_key", "") or ""
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


def run_agent_chat(
    system_instructions: str,
    user_message: str,
    provider: str | None = None,
    model_id: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> str | None:
    """
    Run an AGNO agent with the given system prompt and user message; return response content.
    Uses get_agno_model() for vendor-agnostic model. Returns None on missing key or LLM error.
    """
    try:
        model = get_agno_model(
            provider=provider,
            model_id=model_id,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except ValueError:
        return None

    try:
        from agno.agent import Agent

        agent = Agent(model=model, instructions=system_instructions)
        response = agent.run(user_message)
        if response and hasattr(response, "content"):
            out = response.content
            return (out if isinstance(out, str) else str(out)) if out is not None else None
        return None
    except Exception:
        return None
