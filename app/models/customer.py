from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    company_name = Column(String(120), nullable=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=True)
    industry = Column(String(80), default="Technology")
    company_size = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)

    deals = relationship("Deal", back_populates="customer", cascade="all, delete-orphan")
    interactions = relationship("Interaction", back_populates="customer", cascade="all, delete-orphan")

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    channel = Column(String(50), default="email")  # email, call, meeting, chat
    notes = Column(Text, nullable=False)
    sentiment = Column(String(30), default="neutral")  # positive, neutral, negative
    sentiment_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="interactions")
