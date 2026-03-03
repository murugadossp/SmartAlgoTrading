"""Portfolio parse agent: extract holdings from any broker CSV/Excel via LLM (AGNO, structured output)."""
from __future__ import annotations

from app.agents.base_agent import BaseAgent
from app.models.responses import PortfolioParseResult

AGENT_NAME = "portfolio_parse_agent"
_agent = BaseAgent(AGENT_NAME, output_schema=PortfolioParseResult)


def run_portfolio_parse(content_text: str, filename_hint: str = "") -> PortfolioParseResult | None:
    """
    Parse portfolio file content (CSV or Excel-as-text) with LLM; return structured holdings or None.
    Returns None if agent config missing, no API key, LLM fails, or response does not validate.
    """
    if not (content_text or "").strip():
        return None
    user_message = content_text.strip()
    if filename_hint:
        user_message = f"Filename: {filename_hint}\n\n{user_message}"

    result = _agent.run(user_message)
    return result if isinstance(result, PortfolioParseResult) else None
