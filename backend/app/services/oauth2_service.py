"""OAuth2 service for external authentication"""
from sqlmodel import Session, select
from app.models.oauth2 import OAuth2Provider
from app.models.user import User
from app.core.security import JWTHandler
import requests


class OAuth2Service:
    """Handle OAuth2 authentication flows"""

    @staticmethod
    def handle_google_callback(session: Session, code: str, client_id: str, client_secret: str) -> dict:
        """Handle Google OAuth2 callback"""
        # Exchange code for token (simplified)
        # In production, implement full OAuth2 flow with proper validation
        raise NotImplementedError("OAuth2 callback handling requires full implementation")

    @staticmethod
    def link_oauth_account(
        session: Session, user_id: int, provider: str, provider_user_id: str, access_token: str
    ) -> OAuth2Provider:
        """Link OAuth account to existing user"""
        oauth_account = OAuth2Provider(
            provider_name=provider,
            provider_user_id=provider_user_id,
            user_id=user_id,
            access_token=access_token,
        )
        session.add(oauth_account)
        session.commit()
        session.refresh(oauth_account)
        return oauth_account

    @staticmethod
    def get_oauth_account(
        session: Session, provider: str, provider_user_id: str
    ) -> OAuth2Provider:
        """Get OAuth account by provider"""
        oauth_account = session.exec(
            select(OAuth2Provider).where(
                (OAuth2Provider.provider_name == provider)
                & (OAuth2Provider.provider_user_id == provider_user_id)
            )
        ).first()
        return oauth_account

    @staticmethod
    def create_or_link_user(
        session: Session, provider: str, provider_user_id: str, email: str, access_token: str
    ) -> tuple[User, dict]:
        """Create new user or link OAuth to existing user"""
        # Check if OAuth account already linked
        oauth_account = OAuth2Service.get_oauth_account(session, provider, provider_user_id)
        if oauth_account:
            user = session.exec(select(User).where(User.id == oauth_account.user_id)).first()
            tokens = JWTHandler.create_access_token({"sub": str(user.id), "email": user.email})
            return user, {"access_token": tokens, "token_type": "bearer"}

        # Check if email exists
        existing_user = session.exec(select(User).where(User.email == email)).first()
        if existing_user:
            # Link OAuth to existing account
            OAuth2Service.link_oauth_account(session, existing_user.id, provider, provider_user_id, access_token)
            tokens = JWTHandler.create_access_token(
                {"sub": str(existing_user.id), "email": existing_user.email}
            )
            return existing_user, {"access_token": tokens, "token_type": "bearer"}

        # Create new user with OAuth
        new_user = User(
            email=email,
            password_hash="",  # No password for OAuth users
            subscription_tier="free",
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Link OAuth account
        OAuth2Service.link_oauth_account(session, new_user.id, provider, provider_user_id, access_token)

        tokens = JWTHandler.create_access_token({"sub": str(new_user.id), "email": new_user.email})
        return new_user, {"access_token": tokens, "token_type": "bearer"}
