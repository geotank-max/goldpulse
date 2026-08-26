from pydantic import BaseModel
from datetime import datetime

class GoldPrice (BaseModel):
    symbol: str
    price: float
    change: float
    change_percent: float
    timestamp: datetime

class GoldPricePoint(BaseModel):
    timestamp: datetime
    price: float

class GoldHistoryResponse(BaseModel):
    symbol: str
    unit: str
    currency: str
    data: list[GoldPricePoint]

