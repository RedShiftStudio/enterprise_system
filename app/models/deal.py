from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    amount = Column(Float, default=0.0)
    stage = Column(String(50), default="new")  # new, qualification, proposal, negotiation, closed_won, closed_lost
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    # AI-вычисляемые поля
    lead_score = Column(Float, default=0.0)             # 0.0 - 100.0
    win_probability = Column(Float, default=0.0)        # 0.0 - 1.0
    recommended_action = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="deals")
