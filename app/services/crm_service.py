from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.customer import Customer, Interaction
from app.models.deal import Deal
from app.schemas.customer import CustomerCreate, InteractionCreate
from app.schemas.deal import DealCreate, DealUpdate
from app.services.ai_service import AIService

class CRMService:
    @staticmethod
    async def create_customer(db: AsyncSession, data: CustomerCreate) -> Customer:
        customer = Customer(**data.model_dump())
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer

    @staticmethod
    async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 50):
        result = await db.execute(select(Customer).options(selectinload(Customer.interactions)).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def log_interaction(db: AsyncSession, data: InteractionCreate) -> Interaction:
        sentiment_analysis = AIService.analyze_sentiment(data.notes)
        interaction = Interaction(
            customer_id=data.customer_id,
            channel=data.channel,
            notes=data.notes,
            sentiment=sentiment_analysis["sentiment"],
            sentiment_score=sentiment_analysis["score"]
        )
        db.add(interaction)
        await db.commit()
        await db.refresh(interaction)
        return interaction

    @staticmethod
    async def create_deal(db: AsyncSession, data: DealCreate) -> Deal:
        # Получаем данные компании для AI скоринга
        cust_query = await db.execute(select(Customer).options(selectinload(Customer.interactions)).filter_by(id=data.customer_id))
        customer = cust_query.scalar_one_or_none()
        
        company_size = customer.company_size if customer else 10
        sentiments = [i.sentiment_score for i in customer.interactions] if customer else []
        
        ai_res = AIService.score_deal(data.amount, data.stage or "new", company_size, sentiments)

        deal = Deal(
            title=data.title,
            amount=data.amount,
            stage=data.stage,
            customer_id=data.customer_id,
            lead_score=ai_res["lead_score"],
            win_probability=ai_res["win_probability"],
            recommended_action=ai_res["recommended_action"]
        )
        db.add(deal)
        await db.commit()
        await db.refresh(deal)
        return deal

    @staticmethod
    async def get_deals(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(Deal).offset(skip).limit(limit))
        return result.scalars().all()
