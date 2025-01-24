import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.character.application.use_cases.create_character import CreateCharacterUseCase
from app.character.domain.entities.character import Character
from app.character.infrastructure.repositories.character_repository import (
    CharacterRepository,
)
from tests.utils.fakers import CharacterFactory


@pytest.fixture(scope="function")
async def created_character(async_db_session: AsyncSession) -> Character:
    character_factory = CharacterFactory.create()

    character_repository = CharacterRepository(async_db_session)
    use_case = CreateCharacterUseCase(character_repository)

    character = await use_case.execute(
        name=character_factory.name,
        favorite_color=character_factory.favorite_color,
        animal_friend=character_factory.animal_friend,
        superpower=character_factory.superpower,
        hobby=character_factory.hobby,
        personality=character_factory.personality,
    )

    return character
