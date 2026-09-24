Write-Host "Starting DeltaFunc AI Router Microservices..."

$env:PYTHONPATH="c:\Users\shadi\RiderProjects\deltafunc_ai_router"
$GROQ_KEY="your_groq_api_key_here"

# 1. Start Celery (Offer Analyzer)
Start-Process powershell -ArgumentList "-NoExit -Command "cd c:\Users\shadi\RiderProjects\deltafunc_ai_router; .\venv\Scripts\activate; set GROQ_API_KEY=$GROQ_KEY; celery -A services.offer_analyzer.src.celery_app worker -l info -P threads""

# 2. Start FastAPI (Offer Analyzer Gateway on 8000)
Start-Process powershell -ArgumentList "-NoExit -Command "cd c:\Users\shadi\RiderProjects\deltafunc_ai_router; .\venv\Scripts\activate; uvicorn services.offer_analyzer.src.api:app --host 127.0.0.1 --port 8000""

# 3. Start FastAPI (Manager Assistant Text-to-SQL on 8001)
Start-Process powershell -ArgumentList "-NoExit -Command "cd c:\Users\shadi\RiderProjects\deltafunc_ai_router; .\venv\Scripts\activate; set GROQ_API_KEY=$GROQ_KEY; uvicorn services.manager_assistant.api:app --host 127.0.0.1 --port 8001""

# 4. Start FastAPI (Traffic Router TDS on 8002)
Start-Process powershell -ArgumentList "-NoExit -Command "cd c:\Users\shadi\RiderProjects\deltafunc_ai_router; .\venv\Scripts\activate; uvicorn services.traffic_router.api:app --host 127.0.0.1 --port 8002""

Write-Host "All 4 microservices launched in separate windows using GROQ!"

