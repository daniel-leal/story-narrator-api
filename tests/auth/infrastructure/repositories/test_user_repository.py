import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.infrastructure.persistence.models.user import User as UserModel
from app.auth.infrastructure.repositories.user_repository import UserRepository
from tests.utils.fakers import UserFactory


@pytest.mark.asyncio
async def test_save_user(async_db_session: AsyncSession):
    # Arrange
    user_repository = UserRepository(async_db_session)
    user = UserFactory()

    # Act
    await user_repository.save(user)

    # Assert
    result = await async_db_session.execute(
        select(UserModel).filter_by(email=user.email)
    )
    user_model = result.scalar_one_or_none()

    assert user_model is not None
    assert user_model.name == user.name
    assert user_model.email == user.email
    assert user_model.hashed_password == user.hashed_password
    assert user_model.is_active == user.is_active


@pytest.mark.asyncio
async def test_save_user_duplicate_email(async_db_session: AsyncSession):
    # Arrange
    user_repository = UserRepository(async_db_session)
    user = UserFactory()
    await user_repository.save(user)

    # Act & Assert
    with pytest.raises(IntegrityError):
        duplicate_user = UserFactory(email=user.email)
        await user_repository.save(duplicate_user)


@pytest.mark.asyncio
async def test_get_by_email_found(async_db_session: AsyncSession):
    # Arrange
    user_repository = UserRepository(async_db_session)
    user = UserFactory()
    await user_repository.save(user)

    # Act
    retrieved_user = await user_repository.get_by_email(user.email)

    # Assert
    assert retrieved_user is not None
    assert retrieved_user.name == user.name
    assert retrieved_user.email == user.email
    assert retrieved_user.hashed_password == user.hashed_password
    assert retrieved_user.is_active == user.is_active


@pytest.mark.asyncio
async def test_get_by_email_not_found(async_db_session: AsyncSession):
    # Arrange
    user_repository = UserRepository(async_db_session)

    # Act
    retrieved_user = await user_repository.get_by_email("nonexistent@example.com")

    # Assert
    assert retrieved_user is None
