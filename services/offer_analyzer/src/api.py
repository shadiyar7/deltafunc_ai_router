from fastapi import FastAPI, Depends
from pydantic import BaseModel
from services.offer_analyzer.src.database import init_db
from services.offer_analyzer.src.tasks import process_affiliate_offer

app = FastAPI(title="DeltaFunc AI Offer Router", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    await init_db()

class OfferRequest(BaseModel):
    offer_id: str
    title: str
    description: str = ""

@app.post("/api/v1/offers/process")
async def process_offer(offer: OfferRequest):
    """
    Accepts an incoming affiliate offer and dispatches it to the Celery background queue.
    Returns HTTP 202 immediately.
    """
    task = process_affiliate_offer.delay(offer.model_dump())
    return {"message": "Offer queued for AI processing", "task_id": str(task.id), "status": "Accepted"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

