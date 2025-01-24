from typing import no_type_check

import pytest

from app.character.application.use_cases.create_character import CreateCharacterUseCase
from app.character.domain.entities.character import Character as CharacterEntity
from tests.utils.fakers import CharacterFactory
from tests.utils.mocks import MockCharacterRepository


@pytest.fixture
def mock_character_repository():
    return MockCharacterRepository()


@pytest.mark.asyncio
async def test_create_character_success(mock_character_repository):
    character: CharacterEntity = CharacterFactory.create()

    mock_character_repository.configure_save(character=character)

    use_case = CreateCharacterUseCase(mock_character_repository)

    result = await use_case.execute(
        name=character.name,
        favorite_color=character.favorite_color,
        animal_friend=character.animal_friend,
        superpower=character.superpower,
        hobby=character.hobby,
        personality=character.personality,
    )

    assert result.name == character.name
    assert result.favorite_color == character.favorite_color
    assert result.animal_friend == character.animal_friend
    assert result.superpower == character.superpower
    assert result.hobby == character.hobby
    assert result.personality == character.personality


@pytest.mark.asyncio
@no_type_check
async def test_create_character_missing_name(mock_character_repository):
    character: CharacterEntity = CharacterFactory.create()
    use_case = CreateCharacterUseCase(mock_character_repository)

    with pytest.raises(ValueError):
        await use_case.execute(
            name=None,
            favorite_color=character.favorite_color,
            animal_friend=character.animal_friend,
            superpower=character.superpower,
            hobby=character.hobby,
            personality=character.personality,
        )
