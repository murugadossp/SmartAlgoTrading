"""Market data service: resolve symbol → security_id, fetch OHLC for a list of symbols."""
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from app.data.factory import get_broker_client


def _load_symbol_map() -> dict[str, str]:
    """Load optional symbol → security_id from backend/config/symbols.yaml."""
    base = Path(__file__).resolve().parent.parent.parent
    path = base / "config" / "symbols.yaml"
    if not path.exists():
        return {}
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return data.get("symbol_to_security_id") or {}


def resolve_security_id(symbol: str, symbol_map: dict[str, str] | None = None) -> str:
    """Return broker security_id for symbol; fallback to symbol if not in map."""
    if symbol_map is None:
        symbol_map = _load_symbol_map()
    return symbol_map.get(symbol.strip(), symbol.strip())


def get_ohlc_for_symbols(
    symbols: list[str],
    from_date: str | None = None,
    to_date: str | None = None,
    interval: str = "day",
    exchange_segment: str = "NSE_EQ",
) -> dict[str, list[dict[str, Any]]]:
    """
    Fetch OHLC for each symbol. Returns dict symbol -> list of OHLC candles.
    If broker is unavailable or credentials missing, returns empty lists (caller can use mock).
    """
    if not symbols:
        return {}
    symbol_map = _load_symbol_map()
    if not from_date or not to_date:
        end = datetime.now()
        start = end - timedelta(days=60)
        from_date = from_date or start.strftime("%Y-%m-%d")
        to_date = to_date or end.strftime("%Y-%m-%d")

    result: dict[str, list[dict[str, Any]]] = {s: [] for s in symbols}
    try:
        client = get_broker_client()
    except Exception:
        return result

    for symbol in symbols:
        sec_id = resolve_security_id(symbol, symbol_map)
        try:
            candles = client.get_ohlc(
                security_id=sec_id,
                from_date=from_date,
                to_date=to_date,
                interval=interval,
                exchange_segment=exchange_segment,
            )
            if candles:
                result[symbol] = candles
        except Exception:
            pass
    return result
