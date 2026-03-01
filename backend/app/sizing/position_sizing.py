"""Position sizing: max position value per symbol (e.g. 5--10% of portfolio), suggested quantity from price."""
from typing import Any

# Default max fraction of portfolio per equity position (design: 5--10%)
DEFAULT_MAX_POSITION_PCT = 0.05


def max_position_value(portfolio_amount: float, max_pct: float = DEFAULT_MAX_POSITION_PCT) -> float:
    """Max capital to allocate to a single position (e.g. 5% of portfolio)."""
    if portfolio_amount <= 0:
        return 0.0
    return portfolio_amount * max_pct


def suggested_quantity(price: float, portfolio_amount: float, max_pct: float = DEFAULT_MAX_POSITION_PCT) -> int:
    """Suggested number of shares for one position from portfolio amount and price. Returns 0 if price <= 0."""
    if price <= 0:
        return 0
    max_val = max_position_value(portfolio_amount, max_pct)
    return int(max_val / price)


def apply_sizing_to_results(
    results: list[dict[str, Any]],
    portfolio_amount: float,
    max_pct: float = DEFAULT_MAX_POSITION_PCT,
) -> list[dict[str, Any]]:
    """
    Add suggested_quantity and suggested_amount to each result row that has last_price.
    portfolio_amount can be total or the share allocated to this algo (if allocation is used).
    """
    out = []
    for row in results:
        r = dict(row)
        price = r.get("last_price")
        if price is not None and isinstance(price, (int, float)) and price > 0:
            qty = suggested_quantity(float(price), portfolio_amount, max_pct)
            r["suggested_quantity"] = qty
            r["suggested_amount"] = round(qty * float(price), 2)
        else:
            r["suggested_quantity"] = None
            r["suggested_amount"] = None
        out.append(r)
    return out
