"""Portfolio analyzer: total value, sector mix, concentration, top holdings."""
from typing import Any

# Optional: load symbol -> sector from config; for now we use a small static map or no sector
def _load_sector_map() -> dict[str, str]:
    """Return symbol -> sector. Expand via config file later."""
    return {
        "RELIANCE": "Oil & Gas",
        "TCS": "IT Services",
        "INFY": "IT Services",
        "HDFCBANK": "Banking",
        "ICICIBANK": "Banking",
        "SBIN": "Banking",
        "KOTAKBANK": "Banking",
        "BAJFINANCE": "NBFC",
        "TATASTEEL": "Metals",
        "HINDALCO": "Metals",
        "ONGC": "Oil & Gas",
        "TITAN": "Consumer Discretionary",
        "PIDILITIND": "Chemicals",
    }


def _holding_value(h: dict[str, Any]) -> float:
    """Value for one holding: use 'value' if present else quantity * avg_cost."""
    if h.get("value") is not None:
        return float(h["value"])
    qty = int(h.get("quantity") or 0)
    cost = h.get("avg_cost")
    if cost is not None:
        return qty * float(cost)
    return 0.0


def analyze(holdings: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Given list of { symbol, quantity, avg_cost?, value? }, return:
    total_value, sector_mix (if mapping), concentration (top 5 weight %), top_holdings.
    """
    if not holdings:
        return {
            "total_value": 0.0,
            "sector_mix": [],
            "concentration": {},
            "top_holdings": [],
            "holding_count": 0,
        }

    sector_map = _load_sector_map()
    enriched: list[dict[str, Any]] = []
    for h in holdings:
        val = _holding_value(h)
        sym = (h.get("symbol") or "").strip()
        sector = sector_map.get(sym, "Other")
        enriched.append({
            **h,
            "value": val,
            "sector": sector,
        })

    total = sum(_holding_value(h) for h in enriched)
    for e in enriched:
        e["weight_pct"] = round((e["value"] / total * 100), 2) if total else 0

    # Sector mix: aggregate by sector
    sector_agg: dict[str, float] = {}
    for e in enriched:
        s = e["sector"]
        sector_agg[s] = sector_agg.get(s, 0) + e["value"]
    sector_mix = [
        {"sector": s, "value": round(v, 2), "pct": round(v / total * 100, 2) if total else 0}
        for s, v in sorted(sector_agg.items(), key=lambda x: -x[1])
    ]

    # Top holdings by value
    sorted_holdings = sorted(enriched, key=lambda x: -x["value"])
    top_holdings = sorted_holdings[:10]
    top5 = sorted_holdings[:5]
    concentration = {h["symbol"]: h["weight_pct"] for h in top5} if top5 else {}

    return {
        "total_value": round(total, 2),
        "sector_mix": sector_mix,
        "concentration": concentration,
        "holdings": [
            {"symbol": h["symbol"], "quantity": h["quantity"], "value": h["value"], "weight_pct": h["weight_pct"], "sector": h["sector"]}
            for h in enriched
        ],
        "top_holdings": [
            {"symbol": h["symbol"], "quantity": h["quantity"], "value": h["value"], "weight_pct": h["weight_pct"], "sector": h["sector"]}
            for h in top_holdings
        ],
        "holding_count": len(holdings),
    }
