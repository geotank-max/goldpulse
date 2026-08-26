from fastapi import FastAPI
from app.api.routes import gold

app = FastAPI(title="GoldPulse API")

app.include_router(gold.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "goldpulse-api"}

