"""Abstract interface for broker / market data providers."""
from typing import Any, Protocol


class BrokerClient(Protocol):
    """Protocol for broker or market data provider clients.
    Implementations: Dhan (first), others can be added (e.g. Zerodha).
    """

    def get_ltp(self, security_ids: list[str]) -> dict[str, float]:
        """Return last traded price per security_id. Keys are security_id, values are LTP."""
        ...

    def get_ohlc(
        self,
        security_id: str,
        from_date: str,
        to_date: str,
        interval: str = "day",
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Return OHLC candles for the given security and date range.
        Each candle: open, high, low, close, volume, (optional) timestamp.
        kwargs: provider-specific (e.g. exchange_segment, instrument_type for Dhan).
        """
        ...

    def place_order(
        self,
        security_id: str,
        exchange_segment: str,
        transaction_type: str,
        quantity: int,
        order_type: str,
        product_type: str,
        **kwargs: Any,
    ) -> Any:
        """Place an order. Optional; only when execution is enabled. Returns provider-specific response."""
        ...
