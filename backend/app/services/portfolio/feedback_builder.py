"""Build text summary and suggestions from analyzer output (rule-based). Optional: LLM later."""
from typing import Any


def build_feedback(analysis: dict[str, Any]) -> dict[str, Any]:
    """
    From analyzer output, build feedback: summary (str), suggestions (list[str]).
    Optionally include analysis_html when LLM portfolio research agent is wired (T3.3b).
    """
    total = analysis.get("total_value") or 0
    count = analysis.get("holding_count") or 0
    sector_mix = analysis.get("sector_mix") or []
    concentration = analysis.get("concentration") or {}
    top_holdings = analysis.get("top_holdings") or []

    summary_parts = []
    summary_parts.append(f"Portfolio has {count} holdings with total value ₹{total:,.0f}.")
    if sector_mix:
        top_sectors = sector_mix[:3]
        summary_parts.append(f"Largest sectors: {', '.join(s['sector'] + ' (' + str(s['pct']) + '%)' for s in top_sectors)}.")
    if concentration:
        top_symbol = list(concentration.keys())[0] if concentration else None
        top_pct = list(concentration.values())[0] if concentration else 0
        if top_pct > 20:
            summary_parts.append(f"Concentration: {top_symbol} is {top_pct}% of portfolio.")

    suggestions: list[str] = []
    if concentration:
        for sym, pct in concentration.items():
            if pct > 25:
                suggestions.append(f"Consider reducing concentration in {sym} (currently {pct}% of portfolio).")
    if sector_mix and len(sector_mix) < 3 and count > 5:
        suggestions.append("Portfolio is spread across few sectors; consider diversifying by sector.")
    if count > 15:
        suggestions.append("You have many holdings; consider focusing on a smaller set for easier rebalancing.")
    if not suggestions:
        suggestions.append("Review target allocation and rebalancing bands when you are ready.")

    return {
        "summary": " ".join(summary_parts),
        "suggestions": suggestions,
        "analysis_html": None,  # T3.3b: LLM-generated dashboard HTML when agent is implemented
    }
