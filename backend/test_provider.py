import asyncio
from app.services.gold_provider import GoldPriceProvider

async def main():
    provider = GoldPriceProvider()
    result = await provider.get_current_price()
    print(result)

asyncio.run(main())