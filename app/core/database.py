import contextlib
import logging
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    """
    Manages the lifecycle of the database engine and sessions for asynchronous database
    operations.
    """

    def __init__(self, database_url: str):
        self.engine: AsyncEngine | None = None
        self.session_maker = None
        self.database_url = database_url

    def init_db(self):
        """Initialize the database engine and session maker."""

        self.engine = create_async_engine(self.database_url, echo=True)

        self.session_maker = async_sessionmaker(
            bind=self.engine, autoflush=True, expire_on_commit=False
        )

    async def close(self):
        """Close the database engine."""

        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized.")
        await self.engine.dispose()

        self.engine = None
        self.session_maker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Asynchronously connects to the database and yields an active connection.
        This method ensures that the database engine is initialized before attempting
        to establish a connection. If the engine is not initialized, an exception is
        raised.
        The connection is yielded within a context manager to ensure proper handling
        of the connection lifecycle.

        Yields
        ------
            AsyncIterator[AsyncConnection]: An asynchronous iterator that yields an
            active database connection.

        Raises
        ------
            Exception: If the database engine is not initialized or if there is an error
            during the connection process.
        """

        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized.")
        async with self.engine.begin() as conn:
            try:
                yield conn
            except Exception as e:
                await conn.rollback()
                logger.error(f"Database connection failed: {e}")
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Provides an asynchronous context manager for database sessions.

        Yields
        ------
        AsyncIterator[AsyncSession]
            An asynchronous iterator that yields an instance of AsyncSession.

        Raises
        ------
        Exception
            If the DatabaseSessionManager is not initialized.
        Exception
            If there is an error during the database session, it will be logged and
            re-raised.
        """

        if self.session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized.")

        session = self.session_maker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database connection failed: {e}")
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.get_database_url())


async def get_async_session():
    """
    Asynchronously yields a database session.
    This function is a coroutine that creates an asynchronous database session
    using the session manager and yields it. The session is automatically
    closed when the context is exited.

    Yields
    ------
    session : AsyncSession
        An asynchronous database session.
    """

    async with sessionmanager.session() as session:
        yield session
