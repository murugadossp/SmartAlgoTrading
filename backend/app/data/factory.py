"""Factory for broker / market data client. Returns implementation based on config (e.g. Dhan)."""
from app.config.settings import Settings, get_settings
from app.data.base import BrokerClient
from app.data.dhan_client import DhanBrokerClient


def get_broker_client(settings: Settings | None = None) -> BrokerClient:
    """Return the configured broker client. First implementation: Dhan."""
    settings = settings or get_settings()
    provider = (settings.broker_provider or "dhan").strip().lower()
    if provider == "dhan":
        return DhanBrokerClient(
            access_token=settings.dhan_access_token,
            client_id=settings.dhan_client_id,
        )
    raise ValueError(f"Unknown broker provider: {provider}. Supported: dhan.")
