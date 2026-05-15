"""OAuth2 provider model for external authentication"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class OAuth2Provider(SQLModel, table=True):
    """OAuth2 provider model linking external accounts"""

    id: Optional[int] = Field(default=None, primary_key=True)
    provider_name: str = Field(index=True)  # google, github, facebook
    provider_user_id: str = Field(unique=True, index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    access_token: str  # Should be encrypted in production
    refresh_token: Optional[str] = None  # Should be encrypted if present
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<OAuth2Provider(provider={self.provider_name}, user_id={self.user_id})>"
