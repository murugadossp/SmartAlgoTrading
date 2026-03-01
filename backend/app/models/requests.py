"""Pydantic models for API request bodies."""
from typing import Any

from pydantic import BaseModel, Field


class PortfolioRunRequest(BaseModel):
    """Request body for POST /portfolio/run."""

    amount: float = Field(gt=0, description="Portfolio capital in INR")
    algo_ids: list[str] | None = Field(default=None, description="Algo ids to run; if empty, run all stock algos")
    allocation: dict[str, float] | None = Field(default=None, description="Optional per-algo capital allocation (algo_id -> fraction)")


class HoldingItem(BaseModel):
    """Single holding for rebalance request."""

    symbol: str = Field(..., description="Stock symbol")
    quantity: int = Field(..., ge=0)
    avg_cost: float | None = Field(default=None, description="Average cost per unit")
    value: float | None = Field(default=None, description="Current value (overrides quantity * avg_cost)")


class RebalanceRequest(BaseModel):
    """Request body for POST /portfolio/rebalance."""

    holdings: list[HoldingItem] = Field(..., description="Current holdings")
    target_allocation: dict[str, float] | None = Field(default=None, description="Symbol -> target weight (0-1). If empty, equal weight.")
    strategy: str = Field(default="full", description="'full' or 'bands'")
    band_pct: float = Field(default=0.05, ge=0, le=1, description="Band width for bands strategy (e.g. 0.05 = 5%)")
