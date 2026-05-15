"""Application configuration using Pydantic Settings"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/resume_analyzer_db"

    # JWT Configuration
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # OpenAI Configuration
    openai_api_key: str = ""

    # OAuth2 Configuration
    google_client_id: str = ""
    google_client_secret: str = ""
    github_client_id: str = ""
    github_client_secret: str = ""
    facebook_client_id: str = ""
    facebook_client_secret: str = ""

    # Application Configuration
    frontend_url: str = "http://localhost:5173"
    backend_url: str = "http://localhost:8000"
    environment: str = "development"
    debug: bool = True

    # Rate Limiting
    free_tier_monthly_limit: int = 10
    pro_tier_monthly_limit: int = 100
    enterprise_tier_monthly_limit: int = 1000

    # File Upload
    max_resume_file_size: int = 5242880  # 5MB in bytes
    allowed_resume_formats: str = "pdf,docx"

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_allowed_formats(self) -> list[str]:
        """Return list of allowed resume formats"""
        return [fmt.strip() for fmt in self.allowed_resume_formats.split(",")]

    def get_tier_limit(self, tier: str) -> int:
        """Get monthly analysis limit for subscription tier"""
        tier_map = {
            "free": self.free_tier_monthly_limit,
            "pro": self.pro_tier_monthly_limit,
            "enterprise": self.enterprise_tier_monthly_limit,
        }
        return tier_map.get(tier.lower(), self.free_tier_monthly_limit)


settings = Settings()
