"""User service for user profile and subscription management"""
from sqlmodel import Session, select
from app.models.user import User
from datetime import datetime


class UserService:
    """Handle user operations"""

    @staticmethod
    def get_user_profile(session: Session, user_id: int) -> dict:
        """Get user profile with subscription info"""
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise ValueError("User not found")

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "subscription_tier": user.subscription_tier,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    @staticmethod
    def update_subscription_tier(session: Session, user_id: int, tier: str) -> User:
        """Update user subscription tier"""
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise ValueError("User not found")

        valid_tiers = ["free", "pro", "enterprise"]
        if tier not in valid_tiers:
            raise ValueError(f"Invalid subscription tier. Must be one of: {', '.join(valid_tiers)}")

        user.subscription_tier = tier
        user.updated_at = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
