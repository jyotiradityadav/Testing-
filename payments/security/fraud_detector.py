from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import json
import asyncio
from collections import defaultdict

from ..models.transaction import Transaction
from ..models.payment_method import PaymentMethod
from ..core.payment_processor import PaymentRequest

logger = logging.getLogger(__name__)

@dataclass
class RiskFactor:
    name: str
    weight: float
    threshold: float
    description: str

class FraudDetector:
    def __init__(self, redis_client, ml_model_path: Optional[str] = None):
        self.redis_client = redis_client
        self.risk_factors = self._initialize_risk_factors()
        self.ml_model = self._load_ml_model(ml_model_path) if ml_model_path else None
        self._risk_cache = {}
        self._cache_lock = asyncio.Lock()

    def _initialize_risk_factors(self) -> List[RiskFactor]:
        return [
            RiskFactor(
                name="velocity_check",
                weight=0.3,
                threshold=0.7,
                description="Transaction velocity check"
            ),
            RiskFactor(
                name="amount_check",
                weight=0.2,
                threshold=0.8,
                description="Unusual amount detection"
            ),
            RiskFactor(
                name="location_check",
                weight=0.15,
                threshold=0.6,
                description="Geographic location anomaly"
            ),
            RiskFactor(
                name="device_check",
                weight=0.15,
                threshold=0.7,
                description="Device fingerprint analysis"
            ),
            RiskFactor(
                name="behavior_check",
                weight=0.2,
                threshold=0.75,
                description="User behavior pattern analysis"
            )
        ]

    async def analyze_transaction(
        self,
        payment_request: PaymentRequest,
        payment_method: PaymentMethod
    ) -> float:
        """
        Analyze a transaction for potential fraud using multiple risk factors
        and machine learning model if available.
        """
        try:
            # Check cache first
            cache_key = f"fraud_check:{payment_request.customer_id}:{payment_request.idempotency_key}"
            async with self._cache_lock:
                if cache_key in self._risk_cache:
                    return self._risk_cache[cache_key]

            # Gather risk factors
            risk_scores = await asyncio.gather(
                self._check_transaction_velocity(payment_request),
                self._check_amount_risk(payment_request),
                self._check_location_risk(payment_request),
                self._check_device_risk(payment_request),
                self._check_behavior_pattern(payment_request)
            )

            # Calculate weighted risk score
            weighted_score = self._calculate_weighted_score(risk_scores)

            # Apply ML model if available
            if self.ml_model:
                ml_score = await self._apply_ml_model(payment_request, risk_scores)
                weighted_score = 0.7 * weighted_score + 0.3 * ml_score

            # Cache the result
            async with self._cache_lock:
                self._risk_cache[cache_key] = weighted_score

            return weighted_score

        except Exception as e:
            logger.error(f"Error in fraud analysis: {str(e)}", exc_info=True)
            # Return high risk score in case of errors
            return 0.9

    async def _check_transaction_velocity(
        self,
        payment_request: PaymentRequest
    ) -> Tuple[float, str]:
        """Check for unusual transaction frequency"""
        try:
            # Get recent transactions from Redis
            recent_txns = await self._get_recent_transactions(
                payment_request.customer_id,
                timedelta(hours=24)
            )

            # Calculate velocity metrics
            txn_count = len(recent_txns)
            total_amount = sum(txn.amount for txn in recent_txns)
            avg_amount = total_amount / txn_count if txn_count > 0 else 0

            # Define velocity thresholds
            max_txns_per_day = 10
            max_amount_per_day = 10000

            # Calculate risk score
            txn_risk = min(1.0, txn_count / max_txns_per_day)
            amount_risk = min(1.0, total_amount / max_amount_per_day)

            return max(txn_risk, amount_risk), "velocity_check"

        except Exception as e:
            logger.error(f"Error in velocity check: {str(e)}")
            return 0.5, "velocity_check"

    async def _check_amount_risk(
        self,
        payment_request: PaymentRequest
    ) -> Tuple[float, str]:
        """Check for unusual transaction amounts"""
        try:
            # Get historical transaction data
            historical_txns = await self._get_recent_transactions(
                payment_request.customer_id,
                timedelta(days=30)
            )

            if not historical_txns:
                return 0.5, "amount_check"

            # Calculate amount statistics
            amounts = [txn.amount for txn in historical_txns]
            mean_amount = np.mean(amounts)
            std_amount = np.std(amounts)

            # Calculate z-score for current transaction
            z_score = abs(payment_request.amount - mean_amount) / std_amount if std_amount > 0 else 0

            # Convert z-score to risk score (0 to 1)
            risk_score = min(1.0, z_score / 3)

            return risk_score, "amount_check"

        except Exception as e:
            logger.error(f"Error in amount risk check: {str(e)}")
            return 0.5, "amount_check"

    async def _check_location_risk(
        self,
        payment_request: PaymentRequest
    ) -> Tuple[float, str]:
        """Check for location-based anomalies"""
        try:
            # Get location data from metadata
            location_data = payment_request.metadata.get('location', {})
            if not location_data:
                return 0.5, "location_check"

            # Get recent locations from Redis
            recent_locations = await self.redis_client.get(
                f"user_locations:{payment_request.customer_id}"
            )

            if not recent_locations:
                return 0.5, "location_check"

            # Calculate distance and time-based risk
            distance_risk = self._calculate_distance_risk(
                location_data,
                json.loads(recent_locations)
            )

            return distance_risk, "location_check"

        except Exception as e:
            logger.error(f"Error in location risk check: {str(e)}")
            return 0.5, "location_check"

    async def _check_device_risk(
        self,
        payment_request: PaymentRequest
    ) -> Tuple[float, str]:
        """Check for device fingerprint anomalies"""
        try:
            device_data = payment_request.metadata.get('device', {})
            if not device_data:
                return 0.5, "device_check"

            # Get known devices from Redis
            known_devices = await self.redis_client.get(
                f"user_devices:{payment_request.customer_id}"
            )

            if not known_devices:
                return 0.5, "device_check"

            # Calculate device similarity score
            similarity_score = self._calculate_device_similarity(
                device_data,
                json.loads(known_devices)
            )

            return 1 - similarity_score, "device_check"

        except Exception as e:
            logger.error(f"Error in device risk check: {str(e)}")
            return 0.5, "device_check"

    async def _check_behavior_pattern(
        self,
        payment_request: PaymentRequest
    ) -> Tuple[float, str]:
        """Check for behavioral pattern anomalies"""
        try:
            # Get user behavior data
            behavior_data = payment_request.metadata.get('behavior', {})
            if not behavior_data:
                return 0.5, "behavior_check"

            # Get historical behavior patterns
            historical_patterns = await self.redis_client.get(
                f"user_patterns:{payment_request.customer_id}"
            )

            if not historical_patterns:
                return 0.5, "behavior_check"

            # Calculate behavior pattern risk
            pattern_risk = self._calculate_behavior_risk(
                behavior_data,
                json.loads(historical_patterns)
            )

            return pattern_risk, "behavior_check"

        except Exception as e:
            logger.error(f"Error in behavior pattern check: {str(e)}")
            return 0.5, "behavior_check"

    def _calculate_weighted_score(self, risk_scores: List[Tuple[float, str]]) -> float:
        """Calculate weighted risk score from individual risk factors"""
        total_score = 0.0
        total_weight = 0.0

        for score, factor_name in risk_scores:
            factor = next(f for f in self.risk_factors if f.name == factor_name)
            total_score += score * factor.weight
            total_weight += factor.weight

        return total_score / total_weight if total_weight > 0 else 0.5

    async def _apply_ml_model(
        self,
        payment_request: PaymentRequest,
        risk_scores: List[Tuple[float, str]]
    ) -> float:
        """Apply machine learning model for additional risk assessment"""
        try:
            # Prepare features for ML model
            features = self._prepare_ml_features(payment_request, risk_scores)
            
            # Get prediction from model
            prediction = self.ml_model.predict_proba([features])[0]
            
            return float(prediction[1])  # Return probability of fraud

        except Exception as e:
            logger.error(f"Error in ML model prediction: {str(e)}")
            return 0.5

    def _prepare_ml_features(
        self,
        payment_request: PaymentRequest,
        risk_scores: List[Tuple[float, str]]
    ) -> List[float]:
        """Prepare features for ML model input"""
        # Implementation details for feature preparation
        pass

    async def _get_recent_transactions(
        self,
        customer_id: str,
        time_window: timedelta
    ) -> List[Transaction]:
        """Get recent transactions from cache or database"""
        # Implementation details for transaction retrieval
        pass

    def _calculate_distance_risk(
        self,
        current_location: Dict,
        recent_locations: List[Dict]
    ) -> float:
        """Calculate risk based on location distance"""
        # Implementation details for distance calculation
        pass

    def _calculate_device_similarity(
        self,
        current_device: Dict,
        known_devices: List[Dict]
    ) -> float:
        """Calculate similarity score between devices"""
        # Implementation details for device similarity
        pass

    def _calculate_behavior_risk(
        self,
        current_behavior: Dict,
        historical_patterns: List[Dict]
    ) -> float:
        """Calculate risk based on behavior patterns"""
        # Implementation details for behavior risk calculation
        pass 