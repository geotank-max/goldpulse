from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.services.gold_provider import GoldPriceProvider, GoldProviderError
from app.models.gold_price import GoldPriceRecord

provider = GoldPriceProvider()


async def fetch_and_store_current_price(db: Session) -> GoldPriceRecord:
    """Fetch a live price from the provider. Only persist a new row if the
    price actually changed since the last stored record; otherwise return
    the existing latest row unchanged."""
    live_data = await provider.get_current_price()

    last_row = db.execute(
        select(GoldPriceRecord).order_by(GoldPriceRecord.timestamp.desc())
    ).scalars().first()

    if last_row and last_row.price == live_data["price"]:
        return last_row

    record = GoldPriceRecord(
        symbol=live_data["symbol"],
        price=live_data["price"],
        currency="USD",
        unit="ounce",
        timestamp=datetime.now(timezone.utc),
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record