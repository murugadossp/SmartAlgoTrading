"""Rebalancing logic: current vs target weights, suggested trades (buy/sell by symbol)."""
from typing import Any


def _holding_value(h: dict[str, Any]) -> float:
    if h.get("value") is not None:
        return float(h["value"])
    qty = int(h.get("quantity") or 0)
    cost = h.get("avg_cost")
    if cost is not None:
        return qty * float(cost)
    return 0.0


def _price_per_unit(h: dict[str, Any]) -> float | None:
    """Implied price from value/quantity for rebalance quantity calculation."""
    val = _holding_value(h)
    qty = int(h.get("quantity") or 0)
    if qty <= 0:
        return None
    return val / qty


def rebalance(
    holdings: list[dict[str, Any]],
    total_value: float,
    target_allocation: dict[str, float],
    strategy: str = "full",
    band_pct: float = 0.05,
) -> dict[str, Any]:
    """
    Compute current weights, target weights, and list of trades to rebalance.

    - holdings: list of { symbol, quantity, value? or avg_cost }
    - total_value: sum of holding values (must be > 0)
    - target_allocation: symbol -> target weight (0-1). If empty, use equal weight across current holdings.
    - strategy: "full" = rebalance to target; "bands" = only trade when |current - target| > band_pct
    - band_pct: e.g. 0.05 for 5%

    Returns: current_weights, target_weights, trades (symbol, action, quantity, amount).
    """
    if not holdings or total_value <= 0:
        return {
            "current_weights": {},
            "target_weights": {},
            "trades": [],
        }

    symbols = [h.get("symbol") for h in holdings if h.get("symbol")]
    current_weights = {}
    for h in holdings:
        sym = h.get("symbol")
        if not sym:
            continue
        v = _holding_value(h)
        current_weights[sym] = round(v / total_value, 4)

    # Target weights: if not provided, equal weight
    if target_allocation:
        target_weights = {k: float(v) for k, v in target_allocation.items()}
        # Normalize to sum to 1.0
        s = sum(target_weights.values())
        if s > 0:
            target_weights = {k: round(v / s, 4) for k, v in target_weights.items()}
    else:
        n = len(symbols) or 1
        target_weights = {s: round(1.0 / n, 4) for s in symbols}

    # Ensure all current symbols have a target (default 0 if not in target_weights)
    for sym in symbols:
        if sym not in target_weights:
            target_weights[sym] = 0.0

    trades: list[dict[str, Any]] = []
    holdings_by_symbol = {h["symbol"]: h for h in holdings if h.get("symbol")}

    for sym in symbols:
        current = current_weights.get(sym, 0.0)
        target = target_weights.get(sym, 0.0)
        diff = target - current

        if strategy == "bands" and abs(diff) <= band_pct:
            continue
        if abs(diff) < 0.0001:
            continue

        amount = diff * total_value
        h = holdings_by_symbol.get(sym)
        price = _price_per_unit(h) if h else None
        quantity = int(amount / price) if price and price > 0 else None

        if amount > 0:
            trades.append({
                "symbol": sym,
                "action": "buy",
                "amount": round(amount, 2),
                "quantity": quantity,
            })
        else:
            trades.append({
                "symbol": sym,
                "action": "sell",
                "amount": round(-amount, 2),
                "quantity": -quantity if quantity else None,
            })

    return {
        "current_weights": current_weights,
        "target_weights": target_weights,
        "trades": trades,
    }
