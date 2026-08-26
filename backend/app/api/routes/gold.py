from fastapi import APIRouter
from datetime import datetime, timezone, timedelta
from app.schemas.gold import GoldPrice, GoldPricePoint, GoldHistoryResponse, GoldStatistics

router = APIRouter(prefix="/api/gold", tags=["gold"])

VALID_RANGES = {"1d", "1w", "1m", "3m", "6m", "1y"}

@router.get("/current", response_model=GoldPrice)
def get_current_price():
    return GoldPrice(
        symbol="XAUUSD",
        price=3402.52,
        change=18.40,
        change_percent=0.54,
        timestamp=datetime.now(timezone.utc),
    )

@router.get("/history", response_model=GoldHistoryResponse)
def get_history(range_: str = "1d"):
    if range_ not in VALID_RANGES:
        range_ = "1d"

    now = datetime.now(timezone.utc)
    points = [
        GoldPricePoint(
            timestamp=now - timedelta(hours=i),
            price=3400 + (i % 5) * 2.5,
        )
        for i in range(12, 0, -1)
    ]

    return GoldHistoryResponse(
        symbol="XAUUSD",
        unit="ounce",
        currency="USD",
        data=points,
    )

@router.get("/statistics", response_model=GoldStatistics)
def get_statistics():
    now = datetime.now(timezone.utc)
    prices = [3400 + (i % 5) * 2.5 for i in range(12, 0, -1)]

    high = max(prices)
    low = min(prices)
    open_price = prices[0]
    current = prices[-1]
    change_percent = ((current - open_price) / open_price) * 100

    return GoldStatistics(
        symbol="XAUUSD",
        high=high,
        low=low,
        open=open_price,
        current=current,
        change_percent=round(change_percent, 2),
    )