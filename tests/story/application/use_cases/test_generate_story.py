from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.core.dependencies import get_generate_story_use_case
from app.story.domain.exceptions.story_exceptions import (
    CharactersEmptyError,
    InvalidNarrativeStyleError,
    InvalidScenarioError,
    TooManyCharactersError,
)
from tests.utils.fakers import CharacterFactory, ScenarioFactory, StoryFactory


@pytest.fixture
def generate_story_use_case(
    mock_story_generator, mock_character_repository, mock_scenario_repository
):
    return get_generate_story_use_case(
        story_generator=mock_story_generator,
        character_repository=mock_character_repository,
        scenario_repository=mock_scenario_repository,
    )


@pytest.mark.asyncio
async def test_generate_story_success(
    generate_story_use_case,
    mock_character_repository,
    mock_scenario_repository,
    mock_story_generator,
):
    character_ids = [uuid4(), uuid4()]
    scenario_id = uuid4()
    narrative_style = "adventurous"
    characters = [CharacterFactory(), CharacterFactory()]
    scenario = ScenarioFactory()
    generated_story = StoryFactory(
        scenario=scenario, characters=characters, narrative_style=narrative_style
    )

    mock_character_repository.get_by_id.side_effect = characters
    mock_scenario_repository.get_by_id.return_value = scenario
    mock_story_generator.configure_generate(generated_story)

    result = await generate_story_use_case.execute(
        character_ids, scenario_id, narrative_style
    )

    assert await result == generated_story
    mock_character_repository.get_by_id.assert_any_call(character_ids[0])
    mock_character_repository.get_by_id.assert_any_call(character_ids[1])
    mock_scenario_repository.get_by_id.assert_called_once_with(scenario_id)
    mock_story_generator.generate.assert_called_once_with(
        characters, scenario, narrative_style
    )


@pytest.mark.asyncio
async def test_generate_story_empty_character_list(generate_story_use_case):
    character_ids = []
    scenario_id = uuid4()
    narrative_style = "adventurous"

    with pytest.raises(CharactersEmptyError):
        await generate_story_use_case.execute(
            character_ids, scenario_id, narrative_style
        )


@pytest.mark.asyncio
async def test_generate_story_invalid_character_id(
    generate_story_use_case, mock_character_repository
):
    character_ids = [uuid4(), uuid4()]
    scenario_id = uuid4()
    narrative_style = "adventurous"

    mock_character_repository.get_by_id.side_effect = [None, None]

    with pytest.raises(CharactersEmptyError):
        await generate_story_use_case.execute(
            character_ids, scenario_id, narrative_style
        )


@pytest.mark.asyncio
async def test_generate_story_invalid_scenario_id(
    generate_story_use_case, mock_character_repository, mock_scenario_repository
):
    character_ids = [uuid4(), uuid4()]
    scenario_id = uuid4()
    narrative_style = "adventurous"
    characters = [MagicMock(), MagicMock()]

    mock_character_repository.get_by_id.side_effect = characters
    mock_scenario_repository.get_by_id.return_value = None

    with pytest.raises(InvalidScenarioError):
        await generate_story_use_case.execute(
            character_ids, scenario_id, narrative_style
        )


@pytest.mark.asyncio
async def test_generate_story_too_many_characters(
    generate_story_use_case, mock_character_repository, mock_scenario_repository
):
    character_ids = [uuid4() for _ in range(6)]
    scenario_id = uuid4()
    narrative_style = "adventurous"
    characters = [CharacterFactory() for _ in range(6)]

    mock_character_repository.get_by_id.side_effect = characters
    scenario = ScenarioFactory()
    mock_scenario_repository.get_by_id.return_value = scenario

    with pytest.raises(TooManyCharactersError):
        await generate_story_use_case.execute(
            character_ids, scenario_id, narrative_style
        )


@pytest.mark.asyncio
async def test_generate_story_invalid_narrative_style(
    generate_story_use_case, mock_character_repository, mock_scenario_repository
):
    character_ids = [uuid4(), uuid4()]
    scenario_id = uuid4()
    narrative_style = ""

    characters = [CharacterFactory(), CharacterFactory()]
    scenario = ScenarioFactory()

    mock_character_repository.get_by_id.side_effect = characters
    mock_scenario_repository.get_by_id.return_value = scenario

    with pytest.raises(InvalidNarrativeStyleError):
        await generate_story_use_case.execute(
            character_ids, scenario_id, narrative_style
        )
