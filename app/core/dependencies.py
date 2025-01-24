from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.domain.services.auth_service import AuthService
from app.auth.infrastructure.repositories.user_repository import UserRepository
from app.character.application.use_cases.create_character import CreateCharacterUseCase
from app.character.infrastructure.repositories.character_repository import (
    CharacterRepository,
)
from app.core.database import get_async_session


async def get_auth_service(
    db: AsyncSession = Depends(get_async_session),
) -> AuthService:
    """
    Dependency that initializes AuthService with a UserRepository instance.

    Parameters
    ----------
    db : Session
        SQLAlchemy session instance.

    Returns
    -------
    AuthService
        AuthService instance.
    """
    user_repository = UserRepository(db)
    return AuthService(user_repository)


async def get_character_repository(
    db: AsyncSession = Depends(get_async_session),
) -> CharacterRepository:
    return CharacterRepository(db)


async def get_create_character_use_case(
    character_repository: CharacterRepository = Depends(get_character_repository),
) -> CreateCharacterUseCase:
    """
    Provides a CreateCharacterUseCase instance.

    Parameters
    ----------
    db : AsyncSession, optional
        The database session dependency.

    Returns
    -------
    CreateCharacterUseCase
        An instance of CreateCharacterUseCase.
    """
    return CreateCharacterUseCase(character_repository)
