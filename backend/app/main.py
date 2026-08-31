import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app.api.routes import gold
from app.db.database import SessionLocal
from app.db.seed import seed_mock_prices
from app.models.gold_price import GoldPriceRecord
from app.services.gold_service import fetch_and_store_current_price
from app.websocket.manager import manager
from app.services.gold_provider import GoldProviderError

MAX_AGE_HOURS = 1
POLL_INTERVAL_SECONDS = 15

async def price_collector_loop():
    """Runs for the lifetime of the app: periodically fetches a live price,
    stores it via gold_service, and broadcasts it to all connected WS clients."""
    while True:
        db = SessionLocal()
        try:
            record = await fetch_and_store_current_price(db)
            await manager.broadcast({
                "type": "gold_price_update",
                "symbol": record.symbol,
                "price": record.price,
                "timestamp": record.timestamp.isoformat(),
            })
        except GoldProviderError as e:
            print(f"[price_collector_loop] provider error: {e}")
        finally:
            db.close()

        await asyncio.sleep(15)

async def poll_gold_prices(interval_seconds: int = POLL_INTERVAL_SECONDS) -> None:
    """Background task: periodically polls the gold price provider, persists
    new prices when changed, and broadcasts updates over WebSocket."""
    while True:
        try:
            db = SessionLocal()
            try:
                record = await fetch_and_store_current_price(db)
                await manager.broadcast({
                    "type": "gold_price_update",
                    "symbol": record.symbol,
                    "price": record.price,
                    "timestamp": record.timestamp.isoformat(),
                })
            finally:
                db.close()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[poller error] {e}")

        await asyncio.sleep(interval_seconds)


def _ensure_fresh_mock_data() -> None:
    """Reseed when empty or the latest row is older than MAX_AGE_HOURS."""
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(price_collector_loop())
    yield
    task.cancel()


app = FastAPI(title="GoldPulse API", lifespan=lifespan)

app.include_router(gold.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "goldpulse-api"}


@app.websocket("/ws/gold")
async def websocket_gold(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep the connection alive; ignore client messages
    except WebSocketDisconnect:
        manager.disconnect(websocket)
