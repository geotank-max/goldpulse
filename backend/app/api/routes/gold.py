from fastapi import APIRouter
from datetime import datetime, timezone
from app.schemas.gold import GoldPrice

router = APIRouter(prefix="/api/gold", tags=["gold"])

@router.get("/current", response_model=GoldPrice)
def get_current_price():
    return GoldPrice(
        symbol="XAUUSD",
        price=3402.52,
        change=18.40,
        change_percent=0.54,
        timestamp=datetime.now(timezone.utc),
    )

