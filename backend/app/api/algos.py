"""Algos API: list (with segment filter), detail, refresh."""
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.algos.loader import get_algo_by_id, load_algos_config
from app.algos.momentum import run_momentum

router = APIRouter(prefix="/algos", tags=["algos"])

# Cache per algo: algo_id -> last stocks result (for GET detail without re-running)
_algo_stocks_cache: dict[str, list[dict[str, Any]]] = {}


@router.get("")
def list_algos(segment: str | None = Query(default=None, description="Filter by segment: stocks | fno")) -> dict[str, Any]:
    """Return algo list from config; optional filter by segment."""
    algos = load_algos_config()
    out = []
    for a in algos:
        if segment and a.get("segment") != segment:
            continue
        out.append({
            "id": a.get("id"),
            "name": a.get("name"),
            "segment": a.get("segment"),
            "short_description": a.get("short_description"),
        })
    return {"algos": out}


@router.get("/{algo_id}")
def get_algo_detail(algo_id: str) -> dict[str, Any]:
    """Return overview from config (goal, inputs, signals, risk), chart_type, and stocks table."""
    algo = get_algo_by_id(algo_id)
    if not algo:
        raise HTTPException(status_code=404, detail=f"Algo not found: {algo_id}")
    _overview = algo.get("overview") or algo.get("short_description") or ""
    overview = {
        "summary": (_overview if isinstance(_overview, str) else "").strip(),
        "goal": (algo.get("goal") or "").strip() or _overview,
        "inputs": (algo.get("inputs") or "").strip(),
        "signals": (algo.get("signals") or "").strip(),
        "risk": (algo.get("risk") or "").strip(),
    }
    stocks = _algo_stocks_cache.get(algo_id, [])
    return {
        "id": algo.get("id"),
        "name": algo.get("name"),
        "segment": algo.get("segment"),
        "overview": overview,
        "chart_type": algo.get("chart_type"),
        "stocks": stocks,
    }


@router.post("/{algo_id}/refresh")
def refresh_algo(algo_id: str) -> dict[str, Any]:
    """Run algo (no portfolio sizing); cache and return stocks table."""
    global _algo_stocks_cache
    algo = get_algo_by_id(algo_id)
    if not algo:
        raise HTTPException(status_code=404, detail=f"Algo not found: {algo_id}")
    if algo_id == "momentum":
        stocks = run_momentum()
    else:
        stocks = []
    _algo_stocks_cache[algo_id] = stocks
    return {"stocks": stocks}
