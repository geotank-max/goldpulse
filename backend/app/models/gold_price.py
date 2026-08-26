from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db.database import Base

class GoldPriceRecord(Base):
    __tablename__ = "gold_prices"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    
