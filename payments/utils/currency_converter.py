from decimal import Decimal
from typing import Dict, Optional
import aiohttp
import logging
from datetime import datetime, timedelta

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
        """
        Convert amount from one currency to another.
        Returns converted amount with 2 decimal places (rounded half up).
        """
        try:
            # Ensure rates are fresh
            if self._should_update_rates():
                await self._update_rates()

            # Validate currencies
            if from_currency not in self._rates_cache or to_currency not in self._rates_cache:
                raise CurrencyConversionError(f"Unsupported currency pair: {from_currency}/{to_currency}")

            # Get conversion rate
            rate = self._get_rate(from_currency, to_currency)

            # Perform conversion and round
            converted_amount = (amount * rate).quantize(Decimal('0.01'))
            logger.info(f"Converted {amount} {from_currency} to {converted_amount} {to_currency}")
            return converted_amount

        except Exception as e:
            logger.error(f"Currency conversion error: {str(e)}")
            raise CurrencyConversionError(f"Failed to convert currency: {str(e)}")

    def _should_update_rates(self) -> bool:
        """Check if exchange rates need to be updated"""
        if not self._last_update:
            return True
        return (datetime.utcnow() - self._last_update).total_seconds() > self.cache_ttl

    async def _update_rates(self):
        """
        Update exchange rates from external API.
        All rates are relative to USD as the base currency.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.exchangerate-api.com/v4/latest/USD",
                    params={"api_key": self.api_key}
                ) as response:
                    if response.status != 200:
                        raise CurrencyConversionError("Failed to fetch exchange rates")

                    data = await response.json()
                    if "rates" not in data:
                        raise CurrencyConversionError("Exchange rates response missing 'rates' key")
                    self._rates_cache = {
                        currency: Decimal(str(rate))
                        for currency, rate in data["rates"].items()
                    }
                    self._last_update = datetime.utcnow()
                    logger.info(f"[{self._last_update}] Updated currency rates for {len(self._rates_cache)} currencies.")

        except Exception as e:
            logger.error(f"Error updating exchange rates: {str(e)}")
            raise CurrencyConversionError(f"Failed to update exchange rates: {str(e)}")

    def _get_rate(self, from_currency: str, to_currency: str) -> Decimal:
        """
        Get conversion rate between two currencies.
        Converts via USD as the base.
        """
        if from_currency == to_currency:
            return Decimal("1.0")

        from_rate = self._rates_cache[from_currency]
        to_rate = self._rates_cache[to_currency]

        return to_rate / from_rate

---

This is how this task will be automated :
- Step 1: Ensure latest exchange rates are fetched and cached properly, especially for supported currencies.
- Step 2: Improve logging to help monitor/conduct scheduler-based payment conversion checks.
- Step 3: Make sure errors in rate fetching/conversion are properly caught and logged.
- Step 4: Amounts returned are properly rounded and precise for payment flow testing.