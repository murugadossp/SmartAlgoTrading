"""Dhan broker / market data client. First implementation of BrokerClient."""
from typing import Any

from app.data.base import BrokerClient


class DhanBrokerClient:
    """Dhan API implementation of BrokerClient. Uses dhanhq for auth, LTP, OHLC, orders."""

    def __init__(self, access_token: str = "", client_id: str = "") -> None:
        self._access_token = access_token
        self._client_id = client_id
        self._client: Any = None
        self._context: Any = None

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        try:
            from dhanhq import dhanhq
            try:
                from dhanhq import DhanContext
                use_context = True
            except ImportError:
                use_context = False
        except ImportError as e:
            raise RuntimeError(
                "Dhan provider requires the dhanhq package. Install with: pip install dhanhq"
            ) from e
        if not self._access_token or not self._client_id:
            raise ValueError("Dhan client requires DHAN_ACCESS_TOKEN and DHAN_CLIENT_ID.")
        if use_context:
            self._context = DhanContext(self._client_id, self._access_token)
            self._client = dhanhq(self._context)
        else:
            self._client = dhanhq(self._client_id, self._access_token)
        return self._client

    def get_ltp(self, security_ids: list[str]) -> dict[str, float]:
        """Return last traded price per security_id. Uses Dhan ohlc_data or get_ltp if available."""
        if not security_ids:
            return {}
        client = self._get_client()
        out: dict[str, float] = {}
        try:
            if hasattr(client, "get_ltp"):
                resp = client.get_ltp(security_ids)
            elif hasattr(client, "ohlc_data"):
                ids = [int(s) for s in security_ids if str(s).isdigit()]
                if not ids:
                    ids = security_ids
                resp = client.ohlc_data(securities={"NSE_EQ": ids})
            else:
                return out
            if isinstance(resp, dict):
                data = resp.get("data", resp)
                if isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, dict):
                            lp = v.get("lastPrice") or v.get("last_price") or v.get("close") or 0.0
                            out[str(k)] = float(lp)
                elif isinstance(data, list):
                    for item in data:
                        sid = str(item.get("securityId", item.get("security_id", "")))
                        lp = item.get("lastPrice", item.get("last_price", item.get("close", 0.0)))
                        out[sid] = float(lp)
        except Exception:
            pass
        return out

    def get_ohlc(
        self,
        security_id: str,
        from_date: str,
        to_date: str,
        interval: str = "day",
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Return OHLC candles. Uses Dhan historical_daily_data or intraday_minute_data when available."""
        client = self._get_client()
        exchange_segment = kwargs.get("exchange_segment") or "NSE_EQ"
        instrument_type = kwargs.get("instrument_type") or "EQUITY"
        try:
            if interval and "minute" in interval.lower() and hasattr(client, "intraday_minute_data"):
                resp = client.intraday_minute_data(
                    security_id=security_id,
                    exchange_segment=exchange_segment,
                    instrument_type=instrument_type,
                    from_date=from_date,
                    to_date=to_date,
                )
            elif hasattr(client, "historical_daily_data"):
                resp = client.historical_daily_data(
                    security_id=security_id,
                    exchange_segment=exchange_segment,
                    instrument_type=instrument_type,
                    from_date=from_date,
                    to_date=to_date,
                )
            else:
                return []
        except Exception:
            return []
        if isinstance(resp, list):
            return resp
        if isinstance(resp, dict) and "data" in resp:
            return resp["data"]
        return []

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
        """Place order via Dhan place_order. Only when execution is enabled."""
        client = self._get_client()
        return client.place_order(
            security_id=security_id,
            exchange_segment=exchange_segment,
            transaction_type=transaction_type,
            quantity=quantity,
            order_type=order_type,
            product_type=product_type,
            price=kwargs.get("price", 0),
            **{k: v for k, v in kwargs.items() if k != "price"},
        )
