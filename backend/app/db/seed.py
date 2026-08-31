"""Seed gold_prices with mock data so the chart always has points to show.

Temporary until Stage 4 replaces this with a real gold-price provider.
Generates a random-walk price series around ~$3400 covering the last 30 days
(hourly), then replaces whatever is in the table.

Run as a script:  python -m app.db.seed
Or import+call:   seed_mock_prices()
"""
from datetime import datetime, timedelta, timezone
import random

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.gold_price import GoldPriceRecord

HOURS_BACK = 24 * 30  # 30 days of hourly points

SYMBOL = "XAUUSD"
CURRENCY = "USD"
UNIT = "ounce"
BASE_PRICE = 3400.0


def seed_mock_prices(db: Session | None = None, hours_back: int = HOURS_BACK, base: float = BASE_PRICE) -> int:
    owns_session = db is None
    db = db or SessionLocal()
    try:
        db.execute(delete(GoldPriceRecord))

        now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        price = base
        rows: list[GoldPriceRecord] = []
        for i in range(hours_back, -1, -1):
            rows.append(
                GoldPriceRecord(
                    symbol=SYMBOL,
                    price=round(price, 2),
                    currency=CURRENCY,
                    unit=UNIT,
                    timestamp=now - timedelta(hours=i),
                )
            )
            price += random.gauss(0, 4.0)

        db.add_all(rows)
        db.commit()
        return len(rows)
    finally:
        if owns_session:
            db.close()


if __name__ == "__main__":
    n = seed_mock_prices()
    print(f"Seeded {n} mock gold price rows (last {HOURS_BACK // 24} days, hourly).")