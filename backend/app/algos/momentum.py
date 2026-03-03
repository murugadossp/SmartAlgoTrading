"""Momentum algo: watchlist → OHLC → technicals → scoring agent → list of { symbol, suggestion, confidence }."""
from typing import Any

from app.agents.scoring_agent.agent import run_scoring_agent
from app.analysis.technical import compute_technical_view, technical_summary_for_prompt
from app.algos.loader import get_watchlist
from app.services.market_data import get_ohlc_for_symbols


def run_momentum(symbols: list[str] | None = None, news_summary_per_symbol: dict[str, str] | None = None) -> list[dict[str, Any]]:
    """
    Run momentum algo: fetch OHLC for symbols (or momentum watchlist), compute technical view,
    call scoring agent per symbol. Returns list of { symbol, name, suggestion, confidence }.
    """
    if symbols is None:
        symbols = get_watchlist("momentum")
    if not symbols:
        return []
    news_per = news_summary_per_symbol or {}

    ohlc_by_symbol = get_ohlc_for_symbols(symbols)
    results: list[dict[str, Any]] = []
    for symbol in symbols:
        candles = ohlc_by_symbol.get(symbol) or []
        view = compute_technical_view(candles)
        tech_summary = technical_summary_for_prompt(view)
        news_summary = news_per.get(symbol, "")
        scoring = run_scoring_agent(symbol, tech_summary, news_summary)
        results.append({
            "symbol": symbol,
            "name": symbol,
            "suggestion": scoring.suggestion,
            "confidence": scoring.confidence,
            "reasoning": scoring.reasoning,
            "last_price": view.get("last_close"),
        })
    return results
