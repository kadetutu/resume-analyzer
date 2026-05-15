"""Security utilities for JWT and password management"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import jwt
from bcrypt import hashpw, checkpw, gensalt
from app.core.config import settings


class JWTHandler:
    """Handle JWT token creation and validation"""

    @staticmethod
    def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def create_access_token(data: dict) -> str:
        """Create short-lived access token"""
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
        return JWTHandler.create_token(data, expires_delta)

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """Create long-lived refresh token"""
        expires_delta = timedelta(days=settings.refresh_token_expire_days)
        return JWTHandler.create_token(data, expires_delta)


class PasswordHandler:
    """Handle password hashing and verification"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
