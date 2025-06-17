from typing import Dict, Any, Optional
import json
import base64
from datetime import datetime, timedelta
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import jwt
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class EncryptedData(BaseModel):
    """Model for encrypted data with metadata"""
    ciphertext: str
    iv: str
    tag: str
    timestamp: datetime
    version: str = "1.0"

class PaymentEncryption:
    """Handles encryption and decryption of sensitive payment data"""
    
    def __init__(
        self,
        encryption_key: bytes,
        jwt_secret: str,
        key_rotation_days: int = 30
    ):
        self.encryption_key = encryption_key
        self.jwt_secret = jwt_secret
        self.key_rotation_days = key_rotation_days
        self._fernet = Fernet(encryption_key)
        self._rsa_private_key = None
        self._rsa_public_key = None
        self._initialize_rsa_keys()

    def _initialize_rsa_keys(self):
        """Initialize RSA key pair for asymmetric encryption"""
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            public_key = private_key.public_key()
            self._rsa_private_key = private_key
            self._rsa_public_key = public_key
        except Exception as e:
            logger.error(f"Error initializing RSA keys: {str(e)}")
            raise

    def encrypt_payment_data(self, data: Dict[str, Any]) -> str:
        """
        Encrypt sensitive payment data using hybrid encryption
        (RSA for key exchange + AES for data encryption)
        """
        try:
            json_data = json.dumps(data)
            aes_key = Fernet.generate_key()
            f = Fernet(aes_key)
            encrypted_data = f.encrypt(json_data.encode())
            encrypted_key = self._rsa_public_key.encrypt(
                aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            encrypted = EncryptedData(
                ciphertext=base64.b64encode(encrypted_data).decode(),
                iv=base64.b64encode(encrypted_key).decode(),
                tag="",
                timestamp=datetime.utcnow()
            )
            return encrypted.json()
        except Exception as e:
            logger.error(f"Error encrypting payment data: {str(e)}")
            raise

    def decrypt_payment_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt payment data"""
        try:
            encrypted = EncryptedData.parse_raw(encrypted_data)
            encrypted_key = base64.b64decode(encrypted.iv)
            aes_key = self._rsa_private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            f = Fernet(aes_key)
            decrypted_data = f.decrypt(
                base64.b64decode(encrypted.ciphertext)
            )
            return json.loads(decrypted_data.decode())
        except Exception as e:
            logger.error(f"Error decrypting payment data: {str(e)}")
            raise

    def generate_payment_token(
        self,
        payment_data: Dict[str, Any],
        expires_in: Optional[timedelta] = None
    ) -> str:
        """Generate a JWT token for payment data"""
        try:
            if expires_in is None:
                expires_in = timedelta(minutes=15)
            exp = datetime.utcnow() + expires_in
            payload = {
                "data": payment_data,
                "exp": exp,
                "iat": datetime.utcnow()
            }
            token = jwt.encode(
                payload,
                self.jwt_secret,
                algorithm="HS256"
            )
            return token
        except Exception as e:
            logger.error(f"Error generating payment token: {str(e)}")
            raise

    def verify_payment_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a payment token"""
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=["HS256"]
            )
            return payload["data"]
        except jwt.ExpiredSignatureError:
            logger.error("Payment token has expired")
            raise
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid payment token: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error verifying payment token: {str(e)}")
            raise

    def rotate_encryption_key(self) -> bytes:
        """Rotate the encryption key"""
        try:
            new_key = Fernet.generate_key()
            self.encryption_key = new_key
            self._fernet = Fernet(new_key)
            return new_key
        except Exception as e:
            logger.error(f"Error rotating encryption key: {str(e)}")
            raise

    def export_public_key(self) -> str:
        """Export the RSA public key in PEM format"""
        try:
            return self._rsa_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
        except Exception as e:
            logger.error(f"Error exporting public key: {str(e)}")
            raise

    def import_public_key(self, public_key_pem: str):
        """Import an RSA public key in PEM format"""
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode()
            )
            self._rsa_public_key = public_key
        except Exception as e:
            logger.error(f"Error importing public key: {str(e)}")
            raise