import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.domain.entities.user import User
from app.core.dependencies import get_auth_service
from tests.utils.fakers import UserFactory


@pytest.fixture(scope="function")
async def registered_user(async_db_session: AsyncSession) -> User:
    user_factory = UserFactory.create(hashed_password="123123")
    auth_service = get_auth_service(async_db_session)
    await auth_service.register_user(
        user_factory.name, user_factory.email, user_factory.hashed_password
    )

    return user_factory
