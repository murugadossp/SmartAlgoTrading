"""Technical analysis: SMA(20, 50), RSI(14), structured view per symbol from OHLC."""
from typing import Any


def _get_close(candle: dict[str, Any]) -> float:
    """Extract close price from candle (supports different key styles)."""
    for key in ("close", "Close", "c"):
        if key in candle and candle[key] is not None:
            return float(candle[key])
    return 0.0


def _get_ohlc(candle: dict[str, Any]) -> tuple[float, float, float, float]:
    """Return (open, high, low, close) from candle."""
    o = candle.get("open") or candle.get("Open") or candle.get("o") or 0.0
    h = candle.get("high") or candle.get("High") or candle.get("h") or 0.0
    l = candle.get("low") or candle.get("Low") or candle.get("l") or 0.0
    c = _get_close(candle)
    return (float(o), float(h), float(l), float(c))


def sma(closes: list[float], period: int) -> float | None:
    """Simple moving average; returns None if not enough data."""
    if len(closes) < period or period <= 0:
        return None
    return sum(closes[-period:]) / period


def rsi(closes: list[float], period: int = 14) -> float | None:
    """RSI(period). Returns None if not enough data."""
    if len(closes) < period + 1 or period <= 0:
        return None
    gains: list[float] = []
    losses: list[float] = []
    for i in range(1, len(closes)):
        ch = closes[i] - closes[i - 1]
        gains.append(ch if ch > 0 else 0.0)
        losses.append(-ch if ch < 0 else 0.0)
    if len(gains) < period:
        return None
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def compute_technical_view(ohlc: list[dict[str, Any]]) -> dict[str, Any]:
    """
    From a list of OHLC candles (oldest first), compute SMA20, SMA50, RSI(14).
    Returns a structured view: sma_20, sma_50, rsi, last_close, trend (up/down/sideways).
    """
    if not ohlc:
        return {"sma_20": None, "sma_50": None, "rsi": None, "last_close": None, "trend": "unknown"}
    closes = [_get_close(c) for c in ohlc]
    last_close = closes[-1] if closes else None
    sma_20 = sma(closes, 20)
    sma_50 = sma(closes, 50)
    rsi_val = rsi(closes, 14)

    trend = "sideways"
    if sma_20 is not None and sma_50 is not None and last_close is not None:
        if last_close > sma_20 and sma_20 > sma_50:
            trend = "up"
        elif last_close < sma_20 and sma_20 < sma_50:
            trend = "down"

    return {
        "sma_20": round(sma_20, 2) if sma_20 is not None else None,
        "sma_50": round(sma_50, 2) if sma_50 is not None else None,
        "rsi": round(rsi_val, 2) if rsi_val is not None else None,
        "last_close": round(last_close, 2) if last_close is not None else None,
        "trend": trend,
    }


def technical_summary_for_prompt(view: dict[str, Any]) -> str:
    """Format technical view as short text for LLM prompt."""
    parts = []
    if view.get("last_close") is not None:
        parts.append(f"Last close: {view['last_close']}")
    if view.get("sma_20") is not None:
        parts.append(f"SMA(20): {view['sma_20']}")
    if view.get("sma_50") is not None:
        parts.append(f"SMA(50): {view['sma_50']}")
    if view.get("rsi") is not None:
        parts.append(f"RSI(14): {view['rsi']}")
    parts.append(f"Trend: {view.get('trend', 'unknown')}")
    return "; ".join(parts)
