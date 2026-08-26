from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://goldpulse:changeme@{DATABASE_HOST}:5432/goldpulse",
)
DATABASE_URL = DATABASE_URL.replace("localhost", DATABASE_HOST)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()