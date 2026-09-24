import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://admin:root@localhost:5434/deltafunc")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()

class OfferAnalysis(Base):
    __tablename__ = "offer_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(String, index=True)
    title = Column(String)
    category = Column(String)
    risk_score = Column(Float)
    geos = Column(String) # comma separated
    status = Column(String, default="processed")
    created_at = Column(DateTime, default=datetime.utcnow)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
