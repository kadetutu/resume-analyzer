"""Database connection and session management"""
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
from typing import Generator

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)


def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency injection for database session"""
    with Session(engine) as session:
        yield session
