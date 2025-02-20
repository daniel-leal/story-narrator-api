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
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.domain.entities.user import User
from app.core.database import DatabaseSessionManager, get_async_session
from app.core.infrastructure.persistence.models.base import BaseModel
from app.core.settings.config import load_environment
from app.main import app
from tests.utils.mocks import MockAuthService

logger = logging.getLogger(__name__)

settings = load_environment("testing")


@pytest.fixture(autouse=True, scope="session")
def test_settings():
    """
    Automatically set up test environment variables before running tests.
    This ensures consistent settings across all tests.
    """
    # Set environment variables for testing
    os.environ["JWT_SECRET_KEY"] = (
        "nKDXqKoG/pgP2rK7vsz2nHVbzl/2z/vWLGWzgiYcpVZaAQo941tg7Oeg"
    )
    os.environ["JWT_ALGORITHM"] = "HS256"
    os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

    # Load test settings
    test_settings = load_environment("testing")

    # Override the settings in the main application
    from app.core.settings import config

    config.settings = test_settings

    return test_settings


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
    manager = DatabaseSessionManager(settings.get_database_url())
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
    secret_key = settings.JWT_SECRET_KEY
    algorithm = settings.JWT_ALGORITHM

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
    auth_service.secret_key = settings.JWT_SECRET_KEY
    auth_service.algorithm = settings.JWT_ALGORITHM
    auth_service.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
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
