"""Rate limiting service tests"""
import pytest
from app.services.rate_limit_service import RateLimitService
from app.services.auth_service import AuthService
from datetime import datetime


def test_check_subscription_limit(session, test_user_data):
    """Test subscription limit checking"""
    # Create user
    user = AuthService.register_user(session, test_user_data["email"], test_user_data["password"])

    # Check limit for free tier
    can_analyze, message = RateLimitService.check_subscription_limit(session, user.id, "free")
    assert can_analyze is True
    assert "Within limit" in message


def test_log_analysis_usage(session, test_user_data):
    """Test logging analysis usage"""
    # Create user
    user = AuthService.register_user(session, test_user_data["email"], test_user_data["password"])

    # Create rate limit log
    RateLimitService.get_or_create_rate_limit_log(session, user.id, "free")

    # Log usage
    RateLimitService.log_analysis_usage(session, user.id)

    # Get usage info
    usage = RateLimitService.get_usage_info(session, user.id, "free")
    assert usage["used"] == 1
    assert usage["remaining"] == 9  # free tier has 10 limit


def test_get_usage_info(session, test_user_data):
    """Test getting usage information"""
    # Create user
    user = AuthService.register_user(session, test_user_data["email"], test_user_data["password"])

    # Get usage info
    usage = RateLimitService.get_usage_info(session, user.id, "free")
    assert "used" in usage
    assert "limit" in usage
    assert "remaining" in usage
    assert "reset_date" in usage
    assert usage["limit"] == 10  # free tier limit
