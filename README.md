# DeltaFunc AI Router: Affiliate Traffic Automation & Fraud Detection

An enterprise-grade, asynchronous AI router designed for CPA networks and Affiliate Marketing platforms. This system processes incoming affiliate offers in real-time, uses Large Language Models (LLMs) via Structured Output to classify and score the risk of the offers, and triggers automated alerts and workflows for fraudulent traffic.

## 🚀 Architecture
This project implements a highly scalable **Producer-Consumer** architecture:
1. **FastAPI (Gateway):** Accepts incoming offer payloads instantly (HTTP 202) and pushes them to a Redis message broker.
2. **Celery Worker (Consumer):** Picks up tasks from Redis and processes them concurrently.
3. **Gemini AI (LLM):** Semantically analyzes the offer text, identifies the vertical (Nutra, Crypto, iGaming, etc.), and assigns a Fraud Risk Score.
4. **PostgreSQL:** Persists the AI classification results using Async SQLAlchemy (syncpg).
5. **n8n + Telegram:** If an offer exceeds a Risk Score of 80.0%, Celery fires a webhook to a local n8n instance, which instantly alerts the management team in Telegram.

![Architecture Diagram](https://img.shields.io/badge/Architecture-Microservices-blue)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Celery%20%7C%20Redis%20%7C%20Postgres%20%7C%20n8n-success)

## 🛠️ Quick Start

### 1. Start Infrastructure
Start the supporting services (Postgres, Redis, n8n) via Docker Compose:
`ash
docker-compose up -d
`

### 2. Start Application Services
Set your API Key and start the FastAPI gateway and Celery workers:
`ash
# Terminal 1: Start FastAPI
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000

# Terminal 2: Start Celery Worker
set GEMINI_API_KEY=your_google_ai_key
celery -A src.celery_app worker -l info -P threads
`

### 3. Load Testing
To see the system in action, run the traffic simulator which blasts the API with 10 concurrent real-world affiliate offers (mix of clean and scam offers):
`ash
python simulate_traffic.py
`

## 🔮 Future Architecture & Vision (Roadmap)

To evolve this project into a complete AI Automation Hub for a CPA network, the following microservices are planned:

* **Text-to-SQL RAG Analytics:** 
  An AI Assistant for Affiliate Managers. A manager can ask in Telegram: *"Which Crypto offers converted best in Germany last week?"* The bot translates the natural language into a SQL query against the deltafunc PostgreSQL database, executes it, and returns a human-readable summary.
* **AI Creative Generator Pipeline:** 
  When an advertiser uploads a ZIP with raw assets, a background Celery task extracts the text, translates it into 20 languages using Gemini, and prompts Midjourney/DALL-E to generate localized ad banners (for Facebook/TikTok). The finalized creatives are uploaded to an S3 bucket and linked to the offer_id.
* **Smart Traffic Routing (TDS):** 
  Replacing static routing rules with a Predictive ML model (LightGBM/XGBoost). The model caches hot features in Redis and, within 5-10ms of a user click, scores the probability of conversion across 100 available offers, dynamically redirecting the user to the most profitable landing page.

---
*Developed as a demonstration of production-ready AI engineering and async architecture.*
