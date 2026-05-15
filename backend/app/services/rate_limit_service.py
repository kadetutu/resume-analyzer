"""Rate limiting and subscription service"""
from sqlmodel import Session, select
from app.models.subscription import RateLimitLog
from app.core.config import settings
from datetime import datetime, timedelta


class RateLimitService:
    """Handle rate limiting and subscription checks"""

    @staticmethod
    def get_or_create_rate_limit_log(session: Session, user_id: int, tier: str) -> RateLimitLog:
        """Get or create rate limit log for user"""
        # Calculate reset date (first day of next month)
        now = datetime.utcnow()
        if now.month == 12:
            reset_date = datetime(now.year + 1, 1, 1)
        else:
            reset_date = datetime(now.year, now.month + 1, 1)

        log = session.exec(
            select(RateLimitLog).where(RateLimitLog.user_id == user_id)
        ).first()

        if log:
            # Check if reset date has passed
            if datetime.utcnow() >= log.reset_date:
                log.analysis_count = 0
                log.reset_date = reset_date
                log.subscription_tier = tier
                session.add(log)
                session.commit()
        else:
            log = RateLimitLog(
                user_id=user_id,
                analysis_count=0,
                subscription_tier=tier,
                reset_date=reset_date,
            )
            session.add(log)
            session.commit()

        session.refresh(log)
        return log

    @staticmethod
    def check_subscription_limit(session: Session, user_id: int, tier: str) -> tuple[bool, str]:
        """Check if user has exceeded rate limit"""
        log = RateLimitService.get_or_create_rate_limit_log(session, user_id, tier)
        limit = settings.get_tier_limit(tier)

        if log.analysis_count >= limit:
            return False, f"Monthly analysis limit ({limit}) exceeded for {tier} tier"

        return True, "Within limit"

    @staticmethod
    def log_analysis_usage(session: Session, user_id: int) -> None:
        """Log an analysis operation"""
        log = session.exec(
            select(RateLimitLog).where(RateLimitLog.user_id == user_id)
        ).first()

        if log:
            log.analysis_count += 1
            log.updated_at = datetime.utcnow()
            session.add(log)
            session.commit()

    @staticmethod
    def get_usage_info(session: Session, user_id: int, tier: str) -> dict:
        """Get usage information for user"""
        log = RateLimitService.get_or_create_rate_limit_log(session, user_id, tier)
        limit = settings.get_tier_limit(tier)

        return {
            "used": log.analysis_count,
            "limit": limit,
            "remaining": max(0, limit - log.analysis_count),
            "reset_date": log.reset_date.isoformat(),
        }
