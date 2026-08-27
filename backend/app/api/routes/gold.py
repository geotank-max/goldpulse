from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import get_db
from app.models.gold_price import GoldPriceRecord
from datetime import datetime, timezone, timedelta
from app.schemas.gold import GoldPrice, GoldPricePoint, GoldHistoryResponse, GoldStatistics

router = APIRouter(prefix="/api/gold", tags=["gold"])

VALID_RANGES = {"1d", "1w", "1m", "3m", "6m", "1y"}

RANGE_TO_HOURS = {"1d": 24, "1w": 24 * 7, "1m": 24 * 30, "3m": 24 * 90, "6m": 24 * 180, "1y": 24 * 365}

@router.get("/current", response_model=GoldPrice)
def get_current_price(db: Session = Depends(get_db)):
    latest = db.execute(
        select(GoldPriceRecord).order_by(GoldPriceRecord.timestamp.desc())
    ).scalars().first()

    previous = db.execute(
        select(GoldPriceRecord).order_by(GoldPriceRecord.timestamp.desc()).offset(1)
    ).scalars().first()

    change = latest.price - previous.price if previous else 0.0
    change_percent = (change / previous.price * 100) if previous else 0.0

    return GoldPrice(
        symbol=latest.symbol,
        price=latest.price,
        change=round(change, 2),
        change_percent=round(change_percent, 2),
        timestamp=latest.timestamp,
    )

@router.get("/history", response_model=GoldHistoryResponse)
def get_history(range_: str = "1d", db: Session = Depends(get_db)):
    hours = RANGE_TO_HOURS.get(range_, 24)
    since = datetime.now(timezone.utc) - timedelta(hours=hours)

    rows = db.execute(
        select(GoldPriceRecord)
        .where(GoldPriceRecord.timestamp >= since)
        .order_by(GoldPriceRecord.timestamp.asc())
    ).scalars().all()

    return GoldHistoryResponse(
        symbol="XAUUSD",
        unit="ounce",
        currency="USD",
        data=[GoldPricePoint(timestamp=r.timestamp, price=r.price) for r in rows],
    )

@router.get("/statistics", response_model=GoldStatistics)
def get_statistics(db: Session = Depends(get_db)):
    rows = db.execute(
        select(GoldPriceRecord).order_by(GoldPriceRecord.timestamp.asc())
    ).scalars().all()

    prices = [r.price for r in rows]
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