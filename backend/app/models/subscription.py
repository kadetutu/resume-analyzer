"""Subscription and rate limiting models"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class SubscriptionTier(SQLModel, table=True):
    """Subscription tier model defining usage limits"""

    id: Optional[int] = Field(default=None, primary_key=True)
    tier_name: str = Field(unique=True, index=True)  # free, pro, enterprise
    monthly_limit: int  # Analysis operations per month


class RateLimitLog(SQLModel, table=True):
    """Rate limit log for tracking usage"""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    analysis_count: int = Field(default=0)
    subscription_tier: str = Field(default="free")
    reset_date: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<RateLimitLog(user_id={self.user_id}, count={self.analysis_count})>"
