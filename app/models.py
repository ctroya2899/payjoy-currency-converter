from pydantic import BaseModel, Field


class ConversionResponse(BaseModel):
    """JSON contract returned by GET /convert."""

    amount_usd: float = Field(gt=0, description="Original amount in USD")
    currency: str = Field(min_length=3, max_length=3, description="Target currency code (ISO 4217)")
    converted: float = Field(gt=0, description="Amount converted to the target currency")
    rate: float = Field(gt=0, description="Exchange rate used for the conversion")
