from app.exchange_client import get_rate
from app.models import ConversionResponse


async def convert_amount(amount: float, currency: str) -> ConversionResponse:
    """Convert an USD amount to the target currency using the live rate."""
    normalized_currency = currency.strip().upper()

    rate = await get_rate(normalized_currency)
    converted = round(amount * rate, 2)

    return ConversionResponse(
        amount_usd=amount,
        currency=normalized_currency,
        converted=converted,
        rate=rate,
    )