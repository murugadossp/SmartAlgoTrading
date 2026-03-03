"""Scoring agent: load prompt from this folder, substitute placeholders, call LLM via AGNO, return AlgoScoringResponse."""
import json
import re
from typing import Any

from app.agents.base_agent import BaseAgent
from app.models.responses import AlgoScoringResponse

AGENT_NAME = "scoring_agent"
_agent = BaseAgent(AGENT_NAME)


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
    Load scoring_agent prompt and config, substitute placeholders, call LLM via AGNO (vendor-agnostic), return structured response.
    If no API key for configured provider or LLM fails, returns a stub response (Hold, 50, "No LLM available").
    """
    try:
        system_instructions, config = BaseAgent.load_agent_config(AGENT_NAME)
    except FileNotFoundError:
        return AlgoScoringResponse(confidence=50, suggestion="Hold", reasoning="Scoring agent config not found.")

    prompt = _substitute_prompt(system_instructions, symbol, technical_summary, news_summary, config)
    content = _agent.run(f"Score symbol: {symbol}. Return JSON only.", instructions_override=prompt)
    if not content or not isinstance(content, str):
        return AlgoScoringResponse(confidence=50, suggestion="Hold", reasoning="No LLM available or LLM call failed.")

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
