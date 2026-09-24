import json
import os
import asyncio
import httpx
from groq import Groq
from typing import List
from pydantic import BaseModel, Field
from celery.utils.log import get_task_logger
from services.offer_analyzer.src.celery_app import celery_app
from services.offer_analyzer.src.database import AsyncSessionLocal, OfferAnalysis

logger = get_task_logger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

class OfferClassification(BaseModel):
    category: str = Field(description="Primary category: Crypto, Dating, Nutra, Gambling, E-commerce, InfoProduct, or Other")
    risk_score: float = Field(description="0.0 to 100.0. Higher means scam, unrealistic ROI, or non-compliant.")
    geos: List[str] = Field(description="List of target country codes (e.g. ['US', 'CA']). Empty if worldwide.")

async def save_analysis(offer_id: str, title: str, ai_result: OfferClassification):
    async with AsyncSessionLocal() as session:
        analysis = OfferAnalysis(
            offer_id=offer_id,
            title=title,
            category=ai_result.category,
            risk_score=ai_result.risk_score,
            geos=",".join(ai_result.geos)
        )
        session.add(analysis)
        await session.commit()

def send_n8n_webhook(payload: dict):
    webhook_url = "http://localhost:5679/webhook/fraud-alert"
    try:
        httpx.post(webhook_url, json=payload, timeout=5.0)
        logger.info(f"Sent webhook to n8n for high-risk offer: {payload['offer_id']}")
    except Exception as e:
        logger.error(f"Failed to send webhook to n8n: {e}")

@celery_app.task(name="process_affiliate_offer")
def process_affiliate_offer(offer_payload: dict):
    offer_id = offer_payload.get("offer_id")
    title = offer_payload.get("title")
    description = offer_payload.get("description", "")
    
    logger.info(f"Processing offer {offer_id}: {title}")
    
    prompt = f"Analyze the following affiliate offer.\nTitle: {title}\nDescription: {description}\n\nYou must return a valid JSON object matching this schema: {OfferClassification.model_json_schema()}"
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that strictly outputs JSON."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        result_json = json.loads(chat_completion.choices[0].message.content)
        classification = OfferClassification(**result_json)
        
        logger.info(f"AI Result for {offer_id}: {classification}")
        
        asyncio.run(save_analysis(offer_id, title, classification))
        
        if classification.risk_score >= 80.0:
            send_n8n_webhook({
                "offer_id": offer_id,
                "title": title,
                "risk_score": classification.risk_score,
                "category": classification.category,
                "reason": "Automated AI Detection Triggered"
            })
            
        return {"status": "success", "offer_id": offer_id, "ai_result": classification.model_dump()}
        
    except Exception as e:
        logger.error(f"Error processing offer {offer_id}: {e}")
        return {"status": "error", "error": str(e)}


