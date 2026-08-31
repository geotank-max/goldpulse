import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GOLD_API_KEY = os.getenv("GOLD_API_KEY")
GOLD_API_URL = os.getenv("GOLD_API_URL") or "https://www.goldapi.io/api"


class GoldProviderError(Exception):
    """Raised when the external gold-price provider fails or returns bad data."""


class GoldPriceProvider:
    def __init__(self):
        self.headers = {"x-access-token": GOLD_API_KEY}
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=10.0, headers=self.headers)
        return self._client

    async def get_current_price(self) -> dict:
        url = f"{GOLD_API_URL}/XAU/USD"
        client = self._get_client()

        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise GoldProviderError(f"Gold provider request failed: {e}") from e

        data = response.json()

        if "price" not in data:
            raise GoldProviderError(
                f"Unexpected response shape from provider, missing 'price': {data}"
            )

        return {
            "symbol": "XAUUSD",
            "price": data["price"],
            "open_price": data.get("open_price"),
            "high_price": data.get("high_price"),
            "low_price": data.get("low_price"),
        }
