from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
import asyncpg

app = FastAPI(title="Manager Assistant API", version="1.0.0")

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

class ChatRequest(BaseModel):
    query: str

async def execute_sql(sql_query: str):
    try:
        conn = await asyncpg.connect("postgresql://admin:root@localhost:5434/deltafunc")
        rows = await conn.fetch(sql_query)
        await conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/chat")
async def chat_with_assistant(request: ChatRequest):
    prompt = f"""
    You are an AI Assistant for Affiliate Managers.
    The database is PostgreSQL. The table is 'offer_analysis'.
    Schema: id (int), offer_id (text), title (text), category (text), risk_score (float), geos (text).
    
    The user is asking: "{request.query}"
    
    Return ONLY a valid SQL query to answer this. Do NOT wrap it in markdown blockquotes like `sql. Just the raw text.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="openai/gpt-oss-120b",
        )
        sql_query = chat_completion.choices[0].message.content.strip().replace("`sql", "").replace("`", "")
        
        # Execute the SQL
        db_results = await execute_sql(sql_query)
        
        # Now, formulate human response
        human_prompt = f"User asked: {request.query}\nDatabase returned: {db_results}\nFormulate a short, polite answer for the manager based on this data."
        human_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": human_prompt}
            ],
            model="openai/gpt-oss-120b",
        )
        
        return {
            "sql_executed": sql_query,
            "raw_data": db_results,
            "answer": human_completion.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

