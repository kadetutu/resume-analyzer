"""Pydantic schemas for user requests and responses"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserRegisterRequest(BaseModel):
    """User registration request schema"""

    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters")
    username: Optional[str] = None


class UserLoginRequest(BaseModel):
    """User login request schema"""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response schema"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""

    refresh_token: str


class UserResponse(BaseModel):
    """User response schema"""

    id: int
    email: str
    username: Optional[str]
    subscription_tier: str
    created_at: datetime

    class Config:
        from_attributes = True


class OAuth2CallbackRequest(BaseModel):
    """OAuth2 callback request schema"""

    code: str
    state: Optional[str] = None
