import os
import requests
from src.celery_app import celery
from src.database import SessionLocal
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/fraud-alert")

@celery.task(bind=True, max_retries=3)
def process_offer_task(self, offer_id: str, title: str, description: str):
    import time
    time.sleep(2)  # Simulate LLM processing
    
    score = 85.0 if "guaranteed" in title.lower() else 10.0
    
    if score > 80:
        try:
            requests.post(N8N_WEBHOOK, json={"offer_id": offer_id, "score": score}, timeout=5)
        except Exception:
            pass
    
    return {"offer_id": offer_id, "score": score}
