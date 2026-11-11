from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class InteractionBase(BaseModel):
    channel: str
    notes: str

class InteractionCreate(InteractionBase):
    customer_id: int

class InteractionResponse(InteractionBase):
    id: int
    customer_id: int
    sentiment: str
    sentiment_score: float
    created_at: datetime

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    full_name: str
    company_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    industry: Optional[str] = "General"
    company_size: Optional[int] = 10

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    interactions: List[InteractionResponse] = []

    class Config:
        from_attributes = True
