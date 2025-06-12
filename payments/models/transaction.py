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

    def is_payment_successful(self) -> bool:
        """
        Check if the payment was successfully processed.
        """
        return self.status.lower() in {"success", "completed", "paid"}

    def update_status(self, new_status: str):
        """
        Update the status of the transaction and the updated_at timestamp.
        """
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def is_fraudulent(self, threshold: float = 0.8) -> bool:
        """
        Determine if the transaction is likely fraudulent based on the fraud score.
        """
        if self.fraud_score is None:
            return False
        return self.fraud_score >= threshold

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the transaction (for testing/scheduler purposes).
        """
        return {
            "id": self.id,
            "amount": float(self.amount),
            "currency": self.currency,
            "status": self.status,
            "payment_method_id": self.payment_method_id,
            "customer_id": self.customer_id,
            "gateway_transaction_id": self.gateway_transaction_id,
            "metadata": self.metadata,
            "fraud_score": self.fraud_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }