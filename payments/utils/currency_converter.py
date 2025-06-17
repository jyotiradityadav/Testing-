from decimal import Decimal
from typing import Dict, Optional
import aiohttp
import logging
from datetime import datetime

from ..exceptions.payment_exceptions import CurrencyConversionError

logger = logging.getLogger(__name__)

class CurrencyConverter:
    def __init__(self, api_key: str, cache_ttl: int = 3600):
        self.api_key = api_key
        self.cache_ttl = cache_ttl
        self._rates_cache: Dict[str, Decimal] = {}
        self._last_update: Optional[datetime] = None

    async def convert(
        self,
        amount: Decimal,
        from_currency: str,
        to_currency: str
    ) -> Decimal:
        """Convert an amount from one currency to another using the latest exchange rates."""
        try:
            if self._should_update_rates():
                await self._update_rates()

            rate = self._get_rate(from_currency, to_currency)
            converted_amount = amount * rate

            return converted_amount

        except Exception as e:
            logger.error(f"Currency conversion error: {str(e)}")
            raise CurrencyConversionError(f"Failed to convert currency: {str(e)}")

    def _should_update_rates(self) -> bool:
        """Determine whether exchange rates need to be updated based on cache TTL."""
        if not self._last_update:
            return True
        return (datetime.utcnow() - self._last_update).total_seconds() > self.cache_ttl

    async def _update_rates(self):
        """Fetch latest exchange rates from external API and update cache."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.exchangerate-api.com/v4/latest/USD",
                    params={"api_key": self.api_key}
                ) as response:
                    if response.status != 200:
                        raise CurrencyConversionError("Failed to fetch exchange rates")
                    data = await response.json()
                    self._rates_cache = {
                        currency: Decimal(str(rate))
                        for currency, rate in data["rates"].items()
                    }
                    self._last_update = datetime.utcnow()
        except Exception as e:
            logger.error(f"Error updating exchange rates: {str(e)}")
            raise CurrencyConversionError(f"Failed to update exchange rates: {str(e)}")

    def _get_rate(self, from_currency: str, to_currency: str) -> Decimal:
        """Retrieve the conversion rate between two currencies."""
        if from_currency == to_currency:
            return Decimal("1.0")
        if from_currency not in self._rates_cache or to_currency not in self._rates_cache:
            raise CurrencyConversionError(f"Unsupported currency pair: {from_currency}/{to_currency}")
        from_rate = self._rates_cache[from_currency]
        to_rate = self._rates_cache[to_currency]
        return to_rate / from_rate