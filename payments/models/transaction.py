from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional
from sqlalchemy import Column, String, Numeric, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(String, primary_key=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    status = Column(String(50), nullable=False)
    payment_method_id = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)
    gateway_transaction_id = Column(String, nullable=False)
    metadata = Column(JSON, nullable=True)
    fraud_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(
        self,
        amount: Decimal,
        currency: str,
        status: str,
        payment_method_id: str,
        customer_id: str,
        gateway_transaction_id: str,
        metadata: Optional[Dict] = None,
        fraud_score: Optional[float] = None
    ):
        self.id = gateway_transaction_id  # Using gateway transaction ID as primary key
        self.amount = amount
        self.currency = currency
        self.status = status
        self.payment_method_id = payment_method_id
        self.customer_id = customer_id
        self.gateway_transaction_id = gateway_transaction_id
        self.metadata = metadata or {}
        self.fraud_score = fraud_score