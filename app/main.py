from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import engine, Base, get_db
from app.schemas.customer import CustomerCreate, CustomerResponse, InteractionCreate, InteractionResponse
from app.schemas.deal import DealCreate, DealResponse, AIPredictionResponse
from app.services.crm_service import CRMService
from app.services.ai_service import AIService
from app.models.customer import Customer
from app.models.deal import Deal
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

app = FastAPI(
    title="AI CRM System API",
    description="Интеллектуальная CRM платформа с встроенными модулями оценки сделок и анализа коммуникаций.",
    version="1.0.0"
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {"status": "ok", "message": "AI CRM API is running. Visit /docs or open static/index.html"}

# --- Клиенты ---
@app.post("/api/customers", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    return await CRMService.create_customer(db, customer)

@app.get("/api/customers", response_model=List[CustomerResponse])
async def list_customers(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    return await CRMService.get_customers(db, skip, limit)

# --- Коммуникации и AI Sentiment ---
@app.post("/api/interactions", response_model=InteractionResponse)
async def log_interaction(interaction: InteractionCreate, db: AsyncSession = Depends(get_db)):
    return await CRMService.log_interaction(db, interaction)

# --- Сделки и AI Lead Scoring ---
@app.post("/api/deals", response_model=DealResponse)
async def create_deal(deal: DealCreate, db: AsyncSession = Depends(get_db)):
    return await CRMService.create_deal(db, deal)

@app.get("/api/deals", response_model=List[DealResponse])
async def list_deals(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await CRMService.get_deals(db, skip, limit)

@app.get("/api/deals/{deal_id}/ai-prediction", response_model=AIPredictionResponse)
async def get_ai_deal_prediction(deal_id: int, db: AsyncSession = Depends(get_db)):
    deal = await db.get(Deal, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    cust_res = await db.execute(
        select(Customer).options(selectinload(Customer.interactions)).filter_by(id=deal.customer_id)
    )
    customer = cust_res.scalar_one_or_none()
    company_size = customer.company_size if customer else 10
    sentiments = [i.sentiment_score for i in customer.interactions] if customer else []
    
    analysis = AIService.score_deal(deal.amount, deal.stage, company_size, sentiments)
    return AIPredictionResponse(
        deal_id=deal.id,
        lead_score=analysis["lead_score"],
        win_probability=analysis["win_probability"],
        risk_level=analysis["risk_level"],
        recommended_action=analysis["recommended_action"],
        insights=analysis["insights"]
    )

# Подключение статических файлов для UI
try:
    app.mount("/dashboard", StaticFiles(directory="static", html=True), name="static")
except Exception:
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
