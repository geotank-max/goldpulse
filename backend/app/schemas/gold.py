from pydantic import BaseModel
from datetime import datetime

class GoldPrice (BaseModel):
    symbol: str
    price: float
    change: float
    change_percent: float
    timestamp: datetime


    