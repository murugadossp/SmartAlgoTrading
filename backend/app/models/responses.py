"""Pydantic models for agent JSON responses (structured output schema)."""
from typing import Optional

from pydantic import BaseModel, Field


class AlgoScoringResponse(BaseModel):
    """Structured output from scoring agent: confidence, suggestion, reasoning."""

    confidence: int = Field(ge=0, le=100, description="Confidence score 0-100")
    suggestion: str = Field(description="e.g. Strong Buy, Buy, Hold, Sell, Strong Sell")
    reasoning: str = Field(description="Short explanation for the suggestion")


class Holding(BaseModel):
    """Single holding for portfolio parse result (LLM or rule-based)."""

    symbol: str = Field(description="Ticker/symbol (e.g. RELIANCE, TCS). Use 'N/A' if file has no symbol column.")
    stock_name: Optional[str] = Field(default=None, description="Full stock name from file (e.g. 'APOLLO TYRES LTD'). Use 'N/A' or omit if not in file.")
    quantity: int = Field(ge=1, description="Number of shares/units")
    avg_cost: Optional[float] = Field(default=None, description="Average buy price per unit; null if not in file.")
    buy_value: Optional[float] = Field(default=None, description="Total buy value (quantity * avg cost or 'Buy value' column); null if not in file.")
    closing_price: Optional[float] = Field(default=None, description="Closing price per unit; null if not in file.")
    value: Optional[float] = Field(default=None, description="Current value = closing value total (quantity * closing_price or 'Closing value' column); null if not in file.")
    unrealized_pnl: Optional[float] = Field(default=None, description="Unrealised P&L for this holding; null if not in file.")


class PortfolioParseResult(BaseModel):
    """Structured output from portfolio parse agent: list of holdings and optional parse warnings."""

    holdings: list[Holding] = Field(default_factory=list, description="Extracted equity holdings")
    errors: Optional[list[str]] = Field(default=None, description="Optional parse warnings or skipped rows")
    # Optional portfolio-level summary from file (not required for analyze/rebalance; for display only)
    total_unrealized_pnl: Optional[float] = Field(default=None, description="Total unrealized P&L from file if present; else null.")
