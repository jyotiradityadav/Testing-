from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

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

    def is_payment_method_active(self) -> bool:
        """
        Check if the payment method is currently active.
        """
        return self.is_active

    def can_process_payment(self) -> bool:
        """
        Checks if payment method is valid and ready for payment processing.
        Returns True if it can be used for payment, False otherwise.
        """
        # Add more complex checks as needed, for now just check is_active and required fields
        required_fields = [
            self.id,
            self.customer_id,
            self.gateway_token,
            self.type,
            self.preferred_currency
        ]
        if not self.is_active:
            return False
        if any(not field for field in required_fields):
            return False
        return True

---

This is how this task will be automated :
- Step 1: Add methods to check if a payment method is active and can process payments, enabling testing/payment flow validation.
- Step 2: (Optionally) Extend logic later for additional scheduler/testing purposes if needed.