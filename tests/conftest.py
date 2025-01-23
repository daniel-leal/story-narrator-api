import asyncio
import logging
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import DatabaseSessionManager, get_async_session
from app.infrastructure.persistence.models.base import BaseModel
from app.main import app

logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env.test"))

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)


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
