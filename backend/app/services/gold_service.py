from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.services.gold_provider import GoldPriceProvider, GoldProviderError
from app.models.gold_price import GoldPriceRecord

provider = GoldPriceProvider()


async def fetch_and_store_current_price(db: Session) -> GoldPriceRecord:
    """Fetch a live price from the provider, persist it, return the saved row."""
    live_data = await provider.get_current_price()

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