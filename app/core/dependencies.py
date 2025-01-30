from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.domain.services.auth_service import AuthService
from app.auth.infrastructure.repositories.user_repository import UserRepository
from app.character.application.use_cases.create_character import CreateCharacterUseCase
from app.character.infrastructure.repositories.character_repository import (
    CharacterRepository,
)
from app.core.database import get_async_session
from app.story.application.use_cases.create_scenario import CreateScenarioUseCase
from app.story.application.use_cases.get_scenario import GetScenarioUseCase
from app.story.application.use_cases.get_scenarios import GetScenariosUseCase
from app.story.infrastructure.repositories.scenario_repository import ScenarioRepository


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


async def get_scenarios_use_case(
    db: AsyncSession = Depends(get_async_session),
) -> GetScenariosUseCase:
    """
    Provides an instance of GetScenariosUseCase with the given ScenarioRepository
    dependency.

    Parameters
    ----------
    scenario_repository : ScenarioRepository, optional
        The repository dependency for scenarios, by default Depends().

    Returns
    -------
    GetScenariosUseCase
        An instance of GetScenariosUseCase initialized with the provided scenario
        repository.
    """
    scenario_repository = ScenarioRepository(db)
    return GetScenariosUseCase(scenario_repository)


async def get_scenario_use_case(
    db: AsyncSession = Depends(get_async_session),
) -> GetScenarioUseCase:
    """
    Provides an instance of GetScenarioUseCase with the given ScenarioRepository
    dependency.

    Parameters
    ----------
    scenario_repository : ScenarioRepository, optional
        The repository dependency for scenarios, by default Depends().

    Returns
    -------
    GetScenarioUseCase
        An instance of GetScenarioUseCase initialized with the provided scenario
        repository.
    """
    scenario_repository = ScenarioRepository(db)
    return GetScenarioUseCase(scenario_repository)


async def create_scenario_use_case(
    db: AsyncSession = Depends(get_async_session),
) -> CreateScenarioUseCase:
    """
    Creates an instance of CreateScenarioUseCase.

    Parameters
    ----------
    db : AsyncSession, optional
        The asynchronous database session, by default Depends(get_async_session)

    Returns
    -------
    CreateScenarioUseCase
        An instance of CreateScenarioUseCase.
    """
    scenario_repository = ScenarioRepository(db)
    return CreateScenarioUseCase(scenario_repository)
