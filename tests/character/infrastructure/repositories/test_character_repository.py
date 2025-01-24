from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.character.domain.entities.character import Character
from app.character.infrastructure.persistence.models.character import (
    Character as CharacterModel,
)
from app.character.infrastructure.repositories.character_repository import (
    CharacterRepository,
)
from tests.utils.fakers import CharacterFactory


@pytest.mark.asyncio
async def test_save_character(async_db_session: AsyncSession):
    # Arrange
    character_repository = CharacterRepository(async_db_session)
    character: Character = CharacterFactory.create()

    # Act
    user = await character_repository.save(character=character)

    # Assert
    result = await async_db_session.execute(
        select(CharacterModel).filter_by(id=user.id)
    )

    character_model = result.scalar_one_or_none()

    assert character_model is not None
    assert character_model.animal_friend == character.animal_friend
    assert character_model.favorite_color == character.favorite_color
    assert character_model.hobby == character.hobby
    assert character_model.personality == character.personality
    assert character_model.superpower == character.superpower


@pytest.mark.asyncio
async def test_get_character_by_id(async_db_session: AsyncSession):
    # Arrange
    character_repository = CharacterRepository(async_db_session)
    character: Character = CharacterFactory.create()
    await character_repository.save(character=character)

    # Act
    retrieved_character = await character_repository.get_by_id(character.id)  # type: ignore

    # Assert
    assert retrieved_character is not None
    assert retrieved_character.id == character.id
    assert retrieved_character.name == character.name
    assert retrieved_character.animal_friend == character.animal_friend
    assert retrieved_character.favorite_color == character.favorite_color
    assert retrieved_character.hobby == character.hobby
    assert retrieved_character.personality == character.personality
    assert retrieved_character.superpower == character.superpower


@pytest.mark.asyncio
async def test_get_character_by_nonexistent_id(async_db_session: AsyncSession):
    # Arrange
    character_repository = CharacterRepository(async_db_session)
    nonexistent_id = UUID("00000000-0000-0000-0000-000000000000")

    # Act
    retrieved_character = await character_repository.get_by_id(nonexistent_id)

    # Assert
    assert retrieved_character is None
    assert retrieved_character is None
