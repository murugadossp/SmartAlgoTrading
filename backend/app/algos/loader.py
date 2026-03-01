"""Load algo metadata and watchlists from backend/config/algos.yaml."""
from pathlib import Path
from typing import Any

import yaml


def _algos_path() -> Path:
    base = Path(__file__).resolve().parent.parent.parent
    return base / "config" / "algos.yaml"


def load_algos_config() -> list[dict[str, Any]]:
    """Return list of algo dicts: id, name, segment, short_description, overview, watchlist."""
    path = _algos_path()
    if not path.exists():
        return []
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return data.get("algos") or []


def get_algo_by_id(algo_id: str) -> dict[str, Any] | None:
    """Return first algo with matching id, or None."""
    for algo in load_algos_config():
        if algo.get("id") == algo_id:
            return algo
    return None


def get_watchlist(algo_id: str) -> list[str]:
    """Return symbol watchlist for algo; empty list if not found."""
    algo = get_algo_by_id(algo_id)
    if not algo:
        return []
    wl = algo.get("watchlist")
    return list(wl) if isinstance(wl, list) else []
