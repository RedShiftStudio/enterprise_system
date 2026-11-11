from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DealBase(BaseModel):
    title: str
    amount: float
    customer_id: int
    stage: Optional[str] = "new"

class DealCreate(DealBase):
    pass

class DealUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    stage: Optional[str] = None

class DealResponse(DealBase):
    id: int
    lead_score: float
    win_probability: float
    recommended_action: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AIPredictionResponse(BaseModel):
    deal_id: int
    lead_score: float
    win_probability: float
    risk_level: str
    recommended_action: str
    insights: list[str]
