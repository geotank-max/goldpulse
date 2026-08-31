from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from sqlalchemy import select

from app.api.routes import gold
from app.db.database import SessionLocal
from app.db.seed import seed_mock_prices
from app.models.gold_price import GoldPriceRecord

MAX_AGE_HOURS = 1


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ensure_fresh_mock_data()
    yield


def _ensure_fresh_mock_data() -> None:
    """Reseed when empty or the latest row is older than MAX_AGE_HOURS.

    Keeps the demo chart populated while we're on mock data (pre-Stage 4).
    """
    db = SessionLocal()
    try:
        latest = db.execute(
            select(GoldPriceRecord).order_by(GoldPriceRecord.timestamp.desc())
        ).scalars().first()
    finally:
        db.close()

    stale = latest is None or (
        datetime.now(timezone.utc) - latest.timestamp
    ) > timedelta(hours=MAX_AGE_HOURS)

    if stale:
        count = seed_mock_prices()
        print(f"[startup] gold_prices was stale/empty; seeded {count} mock rows")


app = FastAPI(title="GoldPulse API", lifespan=lifespan)

app.include_router(gold.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "goldpulse-api"}



