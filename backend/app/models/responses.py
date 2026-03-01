"""Pydantic models for agent JSON responses (structured output schema)."""
from pydantic import BaseModel, Field


class AlgoScoringResponse(BaseModel):
    """Structured output from scoring agent: confidence, suggestion, reasoning."""

    confidence: int = Field(ge=0, le=100, description="Confidence score 0-100")
    suggestion: str = Field(description="e.g. Strong Buy, Buy, Hold, Sell, Strong Sell")
    reasoning: str = Field(description="Short explanation for the suggestion")
