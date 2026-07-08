from fastapi import APIRouter, HTTPException, Query

from app.exchange_client import ExchangeRateError, UnsupportedCurrencyError
from app.models import ConversionResponse
from app.service import convert_amount

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/convert", response_model=ConversionResponse)
async def convert(
    amount: float = Query(gt=0, description="Amount in USD"),
    currency: str = Query(min_length=3, max_length=3, description="Target currency code, e.g. BRL"),
) -> ConversionResponse:
    try:
        return await convert_amount(amount, currency)
    except UnsupportedCurrencyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ExchangeRateError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc