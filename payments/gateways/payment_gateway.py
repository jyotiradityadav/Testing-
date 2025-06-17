from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from dataclasses import dataclass
from decimal import Decimal
import asyncio
import logging
from datetime import datetime

from ..models.payment_method import PaymentMethod
from ..exceptions.payment_exceptions import PaymentGatewayError

logger = logging.getLogger(__name__)

@dataclass
class GatewayResponse:
    transaction_id: str
    status: str
    amount: Decimal
    currency: str
    gateway_fee: Decimal
    metadata: Dict
    timestamp: datetime
    error_code: Optional[str] = None
    error_message: Optional[str] = None

class PaymentGateway(ABC):
    """Abstract base class for payment gateways"""
    
    @abstractmethod
    async def process(
        self,
        amount: Decimal,
        currency: str,
        payment_method: PaymentMethod,
        metadata: Dict
    ) -> GatewayResponse:
        """Process a payment through the gateway"""
        pass

    @abstractmethod
    async def refund(
        self,
        transaction_id: str,
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None
    ) -> GatewayResponse:
        """Process a refund through the gateway"""
        pass

    @abstractmethod
    async def get_transaction_status(
        self,
        transaction_id: str
    ) -> GatewayResponse:
        """Get the status of a transaction"""
        pass

class StripeGateway(PaymentGateway):
    """Stripe payment gateway implementation"""
    
    def __init__(self, api_key: str, webhook_secret: str):
        self.api_key = api_key
        self.webhook_secret = webhook_secret
        self._client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Stripe client"""
        import stripe
        stripe.api_key = self.api_key
        self._client = stripe

    async def process(
        self,
        amount: Decimal,
        currency: str,
        payment_method: PaymentMethod,
        metadata: Dict
    ) -> GatewayResponse:
        try:
            amount_in_cents = int(amount * 100)
            
            intent = await asyncio.to_thread(
                self._client.PaymentIntent.create,
                amount=amount_in_cents,
                currency=currency.lower(),
                payment_method=payment_method.gateway_token,
                confirm=True,
                metadata=metadata
            )
            fee = Decimal(intent.charges.data[0].fee) / 100 if getattr(intent.charges.data[0], 'fee', None) else Decimal(0)
            return GatewayResponse(
                transaction_id=intent.id,
                status=intent.status,
                amount=amount,
                currency=currency,
                gateway_fee=fee,
                metadata=metadata,
                timestamp=datetime.fromtimestamp(intent.created)
            )
            
        except Exception as e:
            logger.error(f"Stripe payment processing error: {str(e)}")
            raise PaymentGatewayError(f"Stripe payment failed: {str(e)}")

    async def refund(
        self,
        transaction_id: str,
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None
    ) -> GatewayResponse:
        try:
            refund_params = {
                'payment_intent': transaction_id
            }
            if reason:
                refund_params['reason'] = reason
            if amount:
                refund_params['amount'] = int(amount * 100)
            
            refund = await asyncio.to_thread(
                self._client.Refund.create,
                **refund_params
            )
            
            return GatewayResponse(
                transaction_id=refund.id,
                status=refund.status,
                amount=Decimal(refund.amount) / 100,
                currency=refund.currency.upper(),
                gateway_fee=Decimal(0),
                metadata={'reason': reason} if reason else {},
                timestamp=datetime.fromtimestamp(refund.created)
            )
            
        except Exception as e:
            logger.error(f"Stripe refund error: {str(e)}")
            raise PaymentGatewayError(f"Stripe refund failed: {str(e)}")

    async def get_transaction_status(
        self,
        transaction_id: str
    ) -> GatewayResponse:
        try:
            intent = await asyncio.to_thread(
                self._client.PaymentIntent.retrieve,
                transaction_id
            )
            fee = Decimal(intent.charges.data[0].fee) / 100 if getattr(intent.charges.data[0], 'fee', None) else Decimal(0)
            return GatewayResponse(
                transaction_id=intent.id,
                status=intent.status,
                amount=Decimal(intent.amount) / 100,
                currency=intent.currency.upper(),
                gateway_fee=fee,
                metadata=dict(intent.metadata) if hasattr(intent, "metadata") else {},
                timestamp=datetime.fromtimestamp(intent.created)
            )
            
        except Exception as e:
            logger.error(f"Stripe status check error: {str(e)}")
            raise PaymentGatewayError(f"Stripe status check failed: {str(e)}")

class PayPalGateway(PaymentGateway):
    """PayPal payment gateway implementation"""
    
    def __init__(self, client_id: str, client_secret: str, sandbox: bool = False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sandbox = sandbox
        self._client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize PayPal client"""
        import paypalrestsdk
        paypalrestsdk.configure({
            'mode': 'sandbox' if self.sandbox else 'live',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        })
        self._client = paypalrestsdk

    async def process(
        self,
        amount: Decimal,
        currency: str,
        payment_method: PaymentMethod,
        metadata: Dict
    ) -> GatewayResponse:
        try:
            payment = self._client.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": payment_method.gateway_token
                },
                "transactions": [{
                    "amount": {
                        "total": str(amount),
                        "currency": currency
                    },
                    "description": metadata.get('description', '')
                }]
            })
            if payment.create():
                return GatewayResponse(
                    transaction_id=payment.id,
                    status=payment.state,
                    amount=amount,
                    currency=currency,
                    gateway_fee=Decimal(0),
                    metadata=metadata,
                    timestamp=datetime.now()
                )
            else:
                raise PaymentGatewayError(f"PayPal payment creation failed: {payment.error}")
                
        except Exception as e:
            logger.error(f"PayPal payment processing error: {str(e)}")
            raise PaymentGatewayError(f"PayPal payment failed: {str(e)}")

    async def refund(
        self,
        transaction_id: str,
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None
    ) -> GatewayResponse:
        try:
            sale = self._client.Sale.find(transaction_id)
            if amount:
                refund = sale.refund({
                    "amount": {
                        "total": str(amount),
                        "currency": sale.amount.currency
                    }
                })
            else:
                refund = sale.refund({})
                
            if refund.success():
                return GatewayResponse(
                    transaction_id=refund.id,
                    status=refund.state,
                    amount=Decimal(refund.amount.total),
                    currency=refund.amount.currency,
                    gateway_fee=Decimal(0),
                    metadata={'reason': reason} if reason else {},
                    timestamp=datetime.now()
                )
            else:
                raise PaymentGatewayError(f"PayPal refund failed: {refund.error}")
                
        except Exception as e:
            logger.error(f"PayPal refund error: {str(e)}")
            raise PaymentGatewayError(f"PayPal refund failed: {str(e)}")

    async def get_transaction_status(
        self,
        transaction_id: str
    ) -> GatewayResponse:
        try:
            payment = self._client.Payment.find(transaction_id)
            desc = payment.transactions[0].description if hasattr(payment.transactions[0], 'description') else ''
            return GatewayResponse(
                transaction_id=payment.id,
                status=payment.state,
                amount=Decimal(payment.transactions[0].amount.total),
                currency=payment.transactions[0].amount.currency,
                gateway_fee=Decimal(0),
                metadata={'description': desc} if desc else {},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"PayPal status check error: {str(e)}")
            raise PaymentGatewayError(f"PayPal status check failed: {str(e)}")

class BraintreeGateway(PaymentGateway):
    """Braintree payment gateway implementation"""
    
    def __init__(
        self,
        merchant_id: str,
        public_key: str,
        private_key: str,
        sandbox: bool = False
    ):
        self.merchant_id = merchant_id
        self.public_key = public_key
        self.private_key = private_key
        self.sandbox = sandbox
        self._gateway = None
        self._initialize_gateway()

    def _initialize_gateway(self):
        """Initialize Braintree gateway"""
        import braintree
        self._gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment=braintree.Environment.Sandbox if self.sandbox else braintree.Environment.Production,
                merchant_id=self.merchant_id,
                public_key=self.public_key,
                private_key=self.private_key
            )
        )

    async def process(
        self,
        amount: Decimal,
        currency: str,
        payment_method: PaymentMethod,
        metadata: Dict
    ) -> GatewayResponse:
        try:
            result = await asyncio.to_thread(
                self._gateway.transaction.sale,
                {
                    "amount": str(amount),
                    "payment_method_nonce": payment_method.gateway_token,
                    "options": {
                        "submit_for_settlement": True
                    },
                    "custom_fields": metadata
                }
            )
            
            if result.is_success:
                return GatewayResponse(
                    transaction_id=result.transaction.id,
                    status=result.transaction.status,
                    amount=Decimal(result.transaction.amount),
                    currency=result.transaction.currency_iso_code,
                    gateway_fee=Decimal(result.transaction.service_fee_amount or 0),
                    metadata=metadata,
                    timestamp=result.transaction.created_at
                )
            else:
                raise PaymentGatewayError(
                    f"Braintree payment failed: {result.message}"
                )
                
        except Exception as e:
            logger.error(f"Braintree payment processing error: {str(e)}")
            raise PaymentGatewayError(f"Braintree payment failed: {str(e)}")

    async def refund(
        self,
        transaction_id: str,
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None
    ) -> GatewayResponse:
        try:
            if amount:
                result = await asyncio.to_thread(
                    self._gateway.transaction.refund,
                    transaction_id,
                    str(amount)
                )
            else:
                result = await asyncio.to_thread(
                    self._gateway.transaction.refund,
                    transaction_id
                )
                
            if result.is_success:
                return GatewayResponse(
                    transaction_id=result.transaction.id,
                    status=result.transaction.status,
                    amount=Decimal(result.transaction.amount),
                    currency=result.transaction.currency_iso_code,
                    gateway_fee=Decimal(0),
                    metadata={'reason': reason} if reason else {},
                    timestamp=result.transaction.created_at
                )
            else:
                raise PaymentGatewayError(
                    f"Braintree refund failed: {result.message}"
                )
                
        except Exception as e:
            logger.error(f"Braintree refund error: {str(e)}")
            raise PaymentGatewayError(f"Braintree refund failed: {str(e)}")

    async def get_transaction_status(
        self,
        transaction_id: str
    ) -> GatewayResponse:
        try:
            transaction = await asyncio.to_thread(
                self._gateway.transaction.find,
                transaction_id
            )
            
            return GatewayResponse(
                transaction_id=transaction.id,
                status=transaction.status,
                amount=Decimal(transaction.amount),
                currency=transaction.currency_iso_code,
                gateway_fee=Decimal(transaction.service_fee_amount or 0),
                metadata=transaction.custom_fields if hasattr(transaction, "custom_fields") else {},
                timestamp=transaction.created_at
            )
            
        except Exception as e:
            logger.error(f"Braintree status check error: {str(e)}")
            raise PaymentGatewayError(f"Braintree status check failed: {str(e)}")