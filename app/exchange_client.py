import time

import httpx

from app.config import get_settings


class ExchangeRateError(Exception):
    """Raised when the external exchange rate provider fails."""


class UnsupportedCurrencyError(Exception):
    """Raised when the target currency is not supported by the provider."""


_cache: dict[str, tuple[float, float]] = {}


async def get_rate(currency: str) -> float:
    """Return the USD -> currency rate, using a small in-memory cache."""
    settings = get_settings()
    now = time.monotonic()

    cached = _cache.get(currency)
    if cached is not None:
        rate, cached_at = cached
        if now - cached_at < settings.cache_ttl_seconds:
            return rate

    url = f"{settings.exchange_rate_base_url}/{settings.exchange_rate_api_key}/latest/USD"

    try:
        async with httpx.AsyncClient(timeout=settings.http_timeout_seconds) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as exc:
        raise ExchangeRateError("Exchange rate provider is unavailable") from exc

    if data.get("result") != "success":
        raise ExchangeRateError("Exchange rate provider returned an error")

    rates = data["conversion_rates"]
    if currency not in rates:
        raise UnsupportedCurrencyError(f"Currency '{currency}' is not supported")

    rate = rates[currency]
    _cache[currency] = (rate, now)
    return rate