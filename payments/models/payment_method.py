from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'

    id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    gateway_token = Column(String, nullable=False)
    type = Column(String(50), nullable=False)  # e.g., 'credit_card', 'bank_account'
    is_active = Column(Boolean, default=True)
    preferred_currency = Column(String(3), nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(
        self,
        id: str,
        customer_id: str,
        gateway_token: str,
        type: str,
        preferred_currency: str,
        metadata: Optional[dict] = None,
        is_active: bool = True
    ):
        self.id = id
        self.customer_id = customer_id
        self.gateway_token = gateway_token
        self.type = type
        self.preferred_currency = preferred_currency
        self.metadata = metadata or {}
        self.is_active = is_active