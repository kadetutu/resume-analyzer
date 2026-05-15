"""PyTest configuration and fixtures"""
import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from app.core.database import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    """Create test database session"""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with database dependency"""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Test user registration data"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123",
        "username": "testuser",
    }


@pytest.fixture
def test_login_data():
    """Test user login data"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123",
    }
