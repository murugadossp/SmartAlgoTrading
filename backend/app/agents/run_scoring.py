"""Run scoring agent: load prompt from scoring_agent, substitute placeholders, call LLM, return AlgoScoringResponse."""
import json
import re
from typing import Any

from app.agents.base_agent import load_agent_config
from app.config.settings import get_settings
from app.models.responses import AlgoScoringResponse


def _substitute_prompt(template: str, symbol: str, technical_summary: str, news_summary: str, config: dict[str, Any]) -> str:
    """Replace {{placeholder}} in template with values from config and args."""
    suggestion_enum = config.get("suggestion_enum") or ["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]
    confidence_range = config.get("confidence_range") or [0, 100]
    replacements = {
        "symbol": symbol,
        "technical_summary": technical_summary or "No technical data.",
        "news_summary": news_summary or "No news data.",
        "suggestion_enum": ", ".join(suggestion_enum) if isinstance(suggestion_enum, list) else str(suggestion_enum),
        "confidence_range": str(confidence_range),
    }
    out = template
    for key, val in replacements.items():
        out = out.replace("{{" + key + "}}", str(val))
    return out


def _parse_json_from_response(content: str) -> dict[str, Any] | None:
    """Extract JSON object from LLM response (may be wrapped in markdown code block)."""
    content = content.strip()
    match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


def run_scoring_agent(
    symbol: str,
    technical_summary: str,
    news_summary: str = "",
) -> AlgoScoringResponse:
    """
    Load scoring_agent prompt and config, substitute placeholders, call LLM, return structured response.
    If no OpenAI API key or LLM fails, returns a stub response (Hold, 50, "No LLM available").
    """
    try:
        system_instructions, config = load_agent_config("scoring_agent")
    except FileNotFoundError:
        return AlgoScoringResponse(confidence=50, suggestion="Hold", reasoning="Scoring agent config not found.")

    prompt = _substitute_prompt(system_instructions, symbol, technical_summary, news_summary, config)
    settings = get_settings()
    if not settings.openai_api_key:
        return AlgoScoringResponse(confidence=50, suggestion="Hold", reasoning="No LLM API key configured.")

    model = config.get("model") or settings.llm_model or "gpt-4o-mini"
    temperature = config.get("temperature", 0.2)
    max_tokens = config.get("max_tokens", 256)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"Score symbol: {symbol}. Return JSON only."}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = (resp.choices[0].message.content or "").strip()
    except Exception:
        return AlgoScoringResponse(confidence=50, suggestion="Hold", reasoning="LLM call failed.")

    parsed = _parse_json_from_response(content)
    if not parsed:
        return AlgoScoringResponse(confidence=50, suggestion="Hold", reasoning="Could not parse LLM response.")

    try:
        return AlgoScoringResponse(
            confidence=int(parsed.get("confidence", 50)),
            suggestion=str(parsed.get("suggestion", "Hold")).strip(),
            reasoning=str(parsed.get("reasoning", "")).strip() or "No reasoning provided.",
        )
    except Exception:
        return AlgoScoringResponse(confidence=50, suggestion="Hold", reasoning="Invalid LLM response shape.")
