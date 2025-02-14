import asyncio
import logging
import os
from datetime import UTC, datetime
from typing import AsyncGenerator
from uuid import uuid4

import jwt
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.domain.entities.user import User
from app.core.database import DatabaseSessionManager, get_async_session
from app.core.infrastructure.persistence.models.base import BaseModel
from app.main import app
from tests.utils.mocks import MockAuthService

logger = logging.getLogger(__name__)

env_file = os.path.join(os.path.dirname(__file__), "../.env.test")
load_dotenv(dotenv_path=env_file, override=True)


TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Ensure test environment is properly set up before each test."""
    # Verify we're using the test environment
    assert os.getenv("ENV") == "test", "Test environment not properly loaded"
    # Configure logging levels
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)


@pytest.fixture(scope="session")
def event_loop():
    """
    By default, pytest-asyncio may create a new loop for every test function.
    If you want a single loop for the entire session, override it with scope="session".
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def session_manager():
    """
    Create the DatabaseSessionManager in the same event loop used by tests.
    """
    manager = DatabaseSessionManager(TEST_DATABASE_URL)
    manager.init_db()
    yield manager


@pytest_asyncio.fixture(scope="function")
async def async_db_session(session_manager) -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous database session for testing purposes.
    This function sets up a test database session by connecting to the test
    session manager, dropping all tables, creating all tables, and yielding
    a session for use in tests. After the session is used, it drops all tables
    again to clean up.

    Yields
    ------
    AsyncGenerator[AsyncSession, None]
        An asynchronous generator yielding an `AsyncSession` for database operations.
    """
    async with session_manager.connect() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)  # type: ignore
        await conn.run_sync(BaseModel.metadata.create_all)  # type: ignore

    async with session_manager.session() as session:
        yield session
        await session.rollback()

    async with session_manager.connect() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)  # type: ignore


@pytest_asyncio.fixture(scope="function")
async def async_client(async_db_session: AsyncSession):
    """
    Provides an async HTTP client for testing FastAPI routes.
    """

    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        yield async_db_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        async with LifespanManager(app):
            yield client

    app.dependency_overrides.pop(get_async_session, None)


@pytest.fixture
def test_user():
    """Create a test user"""
    return User(
        id=uuid4(),
        name="test_user",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )


@pytest.fixture
def auth_token(test_user):
    """Create a valid JWT token for test user"""
    secret_key = os.getenv("JWT_SECRET_KEY", "test_secret")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    payload = {
        "email": test_user.email,
        "sub": str(test_user.id),
        "exp": datetime.now(UTC).timestamp() + 3600,  # 1 hour expiration
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


@pytest.fixture
def mock_auth_service(test_user):
    """Create a mock auth service with configured user repository"""
    auth_service = MockAuthService()
    auth_service.user_repository.get_by_email.return_value = test_user
    auth_service.configure_verify_token({"email": test_user.email})
    return auth_service


@pytest_asyncio.fixture
async def authenticated_client(async_client, auth_token, mock_auth_service):
    """Create an authenticated client with valid JWT token"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    async_client.headers.update(headers)

    app.state.auth_service = mock_auth_service
    return async_client
