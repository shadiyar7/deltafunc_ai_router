from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import random

app = FastAPI(title="Smart Traffic Router (TDS)", version="2.0.0")

# Load ML Artifacts
MODEL_PATH = "models/tds_model.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    le_geo = joblib.load("models/le_geo.pkl")
    le_device = joblib.load("models/le_device.pkl")
    le_time = joblib.load("models/le_time.pkl")
    le_offer = joblib.load("models/le_offer.pkl")
else:
    model = None

class ClickRequest(BaseModel):
    user_geo: str
    device: str
    time_of_day: str

@app.post("/api/route")
async def route_traffic(click: ClickRequest):
    if not model:
        # Fallback if no model
        return {"offer_id": "fallback_offer", "redirect_url": "https://example.com"}

    try:
        # Get all available offers from the label encoder
        offers = le_offer.classes_
        
        # We need to predict probability of conversion for each offer given user context
        best_offer = None
        highest_prob = -1.0
        
        # Safely transform inputs (handling unseen labels)
        geo_enc = le_geo.transform([click.user_geo])[0] if click.user_geo in le_geo.classes_ else 0
        dev_enc = le_device.transform([click.device])[0] if click.device in le_device.classes_ else 0
        time_enc = le_time.transform([click.time_of_day])[0] if click.time_of_day in le_time.classes_ else 0
        
        for offer in offers:
            off_enc = le_offer.transform([offer])[0]
            
            # Predict
            X_pred = pd.DataFrame([[geo_enc, dev_enc, time_enc, off_enc]], columns=['user_geo_enc', 'device_enc', 'time_enc', 'offer_enc'])
            prob = model.predict_proba(X_pred)[0][1] # Probability of conversion (class 1)
            
            if prob > highest_prob:
                highest_prob = prob
                best_offer = offer
                
        return {
            "action": "redirect",
            "ml_prediction": "success",
            "predicted_conversion_rate": round(highest_prob, 4),
            "offer_id": best_offer,
            "redirect_url": f"https://deltafunc.example.com/track?offer={best_offer}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
