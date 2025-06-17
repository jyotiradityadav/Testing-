from typing import Dict, List, Optional, Union
from datetime import datetime
import asyncio
import logging
from decimal import Decimal
import json

from pydantic import BaseModel, Field, validator
from cryptography.fernet import Fernet
import jwt
from sqlalchemy.orm import Session

from ..models.transaction import Transaction
from ..models.payment_method import PaymentMethod
from ..exceptions.payment_exceptions import (
    PaymentProcessingError,
    InvalidPaymentMethodError,
    InsufficientFundsError,
    FraudDetectionError,
    PaymentGatewayError
)
from ..security.fraud_detector import FraudDetector
from ..security.encryption import PaymentEncryption
from ..gateways.payment_gateway import PaymentGateway
from ..utils.currency_converter import CurrencyConverter
from ..utils.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

class PaymentRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    payment_method_id: str
    customer_id: str
    metadata: Dict = Field(default_factory=dict)
    idempotency_key: Optional[str] = None
    
    @validator('currency')
    def validate_currency(cls, v):
        if not v.isalpha() or not v.isupper():
            raise ValueError('Currency must be a 3-letter uppercase code')
        return v

class PaymentProcessor:
    def __init__(
        self,
        db_session: Session,
        encryption_key: bytes,
        fraud_detector: FraudDetector,
        payment_gateway: PaymentGateway,
        currency_converter: CurrencyConverter,
        rate_limiter: RateLimiter
    ):
        self.db_session = db_session
        self.encryption = PaymentEncryption(encryption_key)
        self.fraud_detector = fraud_detector
        self.payment_gateway = payment_gateway
        self.currency_converter = currency_converter
        self.rate_limiter = rate_limiter
        self._processing_locks: Dict[str, asyncio.Lock] = {}

    async def process_payment(
        self,
        payment_request: PaymentRequest,
        retry_count: int = 3,
        timeout: int = 30
    ) -> Transaction:
        """
        Process a payment with advanced features including:
        - Idempotency handling
        - Rate limiting
        - Fraud detection
        - Currency conversion
        - Retry mechanism
        - Concurrent processing protection
        """
        try:
            # Acquire processing lock for idempotency
            lock = self._processing_locks.setdefault(
                payment_request.idempotency_key or payment_request.payment_method_id,
                asyncio.Lock()
            )
            
            async with lock:
                # Rate limiting check
                await self.rate_limiter.check_rate_limit(payment_request.customer_id)
                
                # Validate payment method
                payment_method = await self._validate_payment_method(
                    payment_request.payment_method_id
                )
                
                # Fraud detection
                fraud_score = await self.fraud_detector.analyze_transaction(
                    payment_request,
                    payment_method
                )
                
                if fraud_score > 0.8:
                    raise FraudDetectionError(
                        f"High fraud risk detected: {fraud_score}"
                    )
                
                # Currency conversion if needed
                converted_amount = await self.currency_converter.convert(
                    payment_request.amount,
                    payment_request.currency,
                    payment_method.preferred_currency
                )
                
                # Process payment with retry mechanism
                for attempt in range(retry_count):
                    try:
                        # Updated async timeout context for Python 3.11+
                        try:
                            ctx_timeout = asyncio.timeout
                        except AttributeError:
                            import async_timeout
                            ctx_timeout = async_timeout.timeout
                        async with ctx_timeout(timeout):
                            # Encrypt sensitive data
                            encrypted_data = self.encryption.encrypt_payment_data(
                                payment_request.dict()
                            )
                            
                            # Process through payment gateway
                            gateway_response = await self.payment_gateway.process(
                                amount=converted_amount,
                                currency=payment_method.preferred_currency,
                                payment_method=payment_method,
                                metadata=encrypted_data
                            )
                            
                            # Create transaction record
                            transaction = Transaction(
                                amount=payment_request.amount,
                                currency=payment_request.currency,
                                status=gateway_response.status,
                                payment_method_id=payment_request.payment_method_id,
                                customer_id=payment_request.customer_id,
                                gateway_transaction_id=gateway_response.transaction_id,
                                metadata=payment_request.metadata,
                                fraud_score=fraud_score
                            )
                            
                            self.db_session.add(transaction)
                            await self.db_session.commit()
                            
                            return transaction
                            
                    except asyncio.TimeoutError:
                        if attempt == retry_count - 1:
                            raise PaymentGatewayError("Payment processing timeout")
                        continue
                    except Exception as e:
                        if attempt == retry_count - 1:
                            raise PaymentProcessingError(f"Payment processing failed: {str(e)}")
                        continue
                        
        except Exception as e:
            logger.error(f"Payment processing error: {str(e)}", exc_info=True)
            raise

    async def _validate_payment_method(self, payment_method_id: str) -> PaymentMethod:
        """Validate payment method and check for any restrictions"""
        payment_method = await self.db_session.get(PaymentMethod, payment_method_id)
        if not payment_method:
            raise InvalidPaymentMethodError(f"Payment method {payment_method_id} not found")
        
        if not payment_method.is_active:
            raise InvalidPaymentMethodError(f"Payment method {payment_method_id} is inactive")
            
        return payment_method

    async def refund_payment(
        self,
        transaction_id: str,
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None
    ) -> Transaction:
        """Process a refund with validation and tracking"""
        # Implementation details for refund processing
        pass

    async def get_transaction_history(
        self,
        customer_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None
    ) -> List[Transaction]:
        """Retrieve transaction history with filtering"""
        # Implementation details for transaction history
        pass

    async def generate_payment_report(
        self,
        start_date: datetime,
        end_date: datetime,
        report_type: str
    ) -> Dict:
        """Generate detailed payment reports"""
        # Implementation details for report generation
        pass