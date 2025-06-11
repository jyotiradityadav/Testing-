class PaymentError(Exception):
    """Base exception for payment-related errors"""
    pass

class PaymentProcessingError(PaymentError):
    """Raised when payment processing fails"""
    pass

class InvalidPaymentMethodError(PaymentError):
    """Raised when payment method is invalid"""
    pass

class InsufficientFundsError(PaymentError):
    """Raised when there are insufficient funds"""
    pass

class FraudDetectionError(PaymentError):
    """Raised when fraud is detected"""
    pass

class PaymentGatewayError(PaymentError):
    """Raised when payment gateway operations fail"""
    pass

class CurrencyConversionError(PaymentError):
    """Raised when currency conversion fails"""
    pass

class RateLimitExceededError(PaymentError):
    """Raised when rate limit is exceeded"""
    pass 