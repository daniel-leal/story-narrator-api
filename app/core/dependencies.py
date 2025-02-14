import os

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.domain.services.auth_service import AuthService
from app.auth.infrastructure.repositories.user_repository import UserRepository
from app.character.application.use_cases.create_character import CreateCharacterUseCase
from app.character.infrastructure.repositories.character_repository import (
    CharacterRepository,
)
from app.core.database import get_async_session
from app.scenario.application.use_cases.create_scenario import CreateScenarioUseCase
from app.scenario.application.use_cases.get_scenario import GetScenarioUseCase
from app.scenario.application.use_cases.get_scenarios import GetScenariosUseCase
from app.scenario.infrastructure.repositories.scenario_repository import (
    ScenarioRepository,
)
from app.story.application.use_cases.generate_story import GenerateStoryUseCase
from app.story.domain.interfaces.story_generator import BaseStoryGenerator
from app.story.infrastructure.ai.chatgpt_story_generator import ChatGPTStoryGenerator
from app.story.infrastructure.ai.llama_story_generator import LlamaStoryGenerator
from app.story.infrastructure.ai.local_story_generator import LocalStoryGenerator


def get_auth_service(
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


def get_character_repository(
    db: AsyncSession = Depends(get_async_session),
) -> CharacterRepository:
    return CharacterRepository(db)


def get_create_character_use_case(
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


def get_scenario_repository(
    db: AsyncSession = Depends(get_async_session),
) -> ScenarioRepository:
    """
    Provides a ScenarioRepository instance.

    Parameters
    ----------
    db : AsyncSession, optional
        The asynchronous database session, by default obtained from Depends(get_async_session).

    Returns
    -------
    ScenarioRepository
        An instance of ScenarioRepository initialized with the provided database session.
    """
    return ScenarioRepository(db)


def get_scenarios_use_case(
    scenario_repository: ScenarioRepository = Depends(get_scenario_repository),
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
    return GetScenariosUseCase(scenario_repository)


def get_scenario_use_case(
    scenario_repository: ScenarioRepository = Depends(get_scenario_repository),
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
    return GetScenarioUseCase(scenario_repository)


def get_create_scenario_use_case(
    scenario_repository: ScenarioRepository = Depends(get_scenario_repository),
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
    return CreateScenarioUseCase(scenario_repository)


def get_story_generator() -> BaseStoryGenerator:  # pragma: no cover
    """
    Returns the appropriate story generator based on configuration.
    """
    generator_type = os.getenv("STORY_GENERATOR", "local").lower()

    if generator_type == "llama":
        return LlamaStoryGenerator()
    elif generator_type == "chatgpt":
        return ChatGPTStoryGenerator()

    return LocalStoryGenerator()


def get_generate_story_use_case(
    story_generator=Depends(get_story_generator),
    character_repository=Depends(get_character_repository),
    scenario_repository=Depends(get_scenario_repository),
) -> GenerateStoryUseCase:
    """
    Provides an instance of GenerateStoryUseCase with its dependencies.

    Parameters
    ----------
    story_generator : StoryGenerator, optional
        The story generator dependency, by default Depends(get_story_generator).
    character_repository : CharacterRepository, optional
        The character repository dependency, by default Depends(get_character_repository).
    scenario_repository : ScenarioRepository, optional
        The scenario repository dependency, by default Depends(get_scenario_repository).

    Returns
    -------
    GenerateStoryUseCase
        An instance of GenerateStoryUseCase initialized with the provided dependencies.
    """
    return GenerateStoryUseCase(
        story_generator, character_repository, scenario_repository
    )
