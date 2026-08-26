from app.db.database import Base, engine
from app.models.gold_price import GoldPriceRecord  # noqa: F401 — import registers the model with Base

Base.metadata.create_all(bind=engine)
print("Tables created.")