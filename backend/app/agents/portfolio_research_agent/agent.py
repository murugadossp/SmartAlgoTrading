"""Portfolio research agent: build dashboard HTML from analyzer output via AGNO (vendor-agnostic). Returns HTML string or None if LLM unavailable."""
import re
from typing import Any

from app.agents.base_agent import BaseAgent

AGENT_NAME = "portfolio_research_agent"
_agent = BaseAgent(AGENT_NAME)


def _format_analysis_for_prompt(analysis: dict[str, Any]) -> str:
    """Turn analyzer output into a short text summary for the LLM."""
    lines = []
    total = analysis.get("total_value") or 0
    count = analysis.get("holding_count") or 0
    lines.append(f"Total value: ₹{total:,.0f}")
    lines.append(f"Holdings: {count}")
    sector_mix = analysis.get("sector_mix") or []
    if sector_mix:
        lines.append("Sector mix:")
        for s in sector_mix[:10]:
            lines.append(f"  - {s.get('sector', '')}: {s.get('pct', 0)}% (₹{s.get('value', 0):,.0f})")
    concentration = analysis.get("concentration") or {}
    if concentration:
        lines.append("Concentration (top weights):")
        for sym, pct in list(concentration.items())[:5]:
            lines.append(f"  - {sym}: {pct}%")
    top_holdings = analysis.get("top_holdings") or []
    if top_holdings:
        lines.append("Top holdings:")
        for h in top_holdings[:10]:
            sym = h.get("symbol", "")
            val = h.get("value")
            wt = h.get("weight_pct")
            val_str = f"₹{val:,.0f}" if val is not None else "—"
            wt_str = f"{wt}%" if wt is not None else "—"
            lines.append(f"  - {sym}: {val_str}, weight {wt_str}")
    return "\n".join(lines)


def _extract_html_from_response(content: str) -> str | None:
    """Get HTML from LLM response; strip markdown code blocks if present."""
    content = (content or "").strip()
    # Remove optional ```html ... ``` wrapper
    match = re.search(r"```(?:html)?\s*\n?(.*?)```", content, re.DOTALL | re.IGNORECASE)
    if match:
        content = match.group(1).strip()
    if not content:
        return None
    return content


def run_portfolio_research(analysis: dict[str, Any]) -> str | None:
    """
    Load portfolio_research_agent prompt and config, send analyzer summary to LLM via AGNO (vendor-agnostic), return dashboard HTML.
    Returns None if agent config missing, no API key for configured provider, or LLM fails.
    """
    context = _format_analysis_for_prompt(analysis)
    raw = _agent.run(f"Generate the dashboard HTML for this portfolio:\n\n{context}")
    if not raw or not isinstance(raw, str):
        return None
    html = _extract_html_from_response(raw)
    return html if html else None
