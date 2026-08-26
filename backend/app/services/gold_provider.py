"""
GoldPriceProvider: the ONLY place that talks to the external gold-price API.

class GoldPriceProvider:
    async def get_current_price(self): ...
    async def get_historical_prices(self, start, end): ...

Swap providers by editing this file only — routers/services never call
the external API directly.
"""
