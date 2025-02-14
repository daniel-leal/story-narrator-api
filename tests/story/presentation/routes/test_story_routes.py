from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.character.infrastructure.persistence.models.character import (
    Character as CharacterModel,
)
from app.scenario.infrastructure.persistence.models.scenario import (
    Scenario as ScenarioModel,
)
from tests.utils.fakers import CharacterFactory, ScenarioFactory, StoryFactory


@pytest.fixture
async def test_characters(async_db_session: AsyncSession):
    """Create and persist test characters"""
    characters = [CharacterFactory() for _ in range(2)]
    for character in characters:
        async_db_session.add(CharacterModel(**character.dict()))
    await async_db_session.commit()
    return characters


@pytest.fixture
async def test_scenario(async_db_session: AsyncSession):
    """Create and persist test scenario"""
    scenario = ScenarioFactory()
    async_db_session.add(ScenarioModel(**scenario.dict()))
    await async_db_session.commit()
    return scenario


@pytest.fixture
async def test_story(test_characters, test_scenario):
    """Create test story with persisted entities"""
    return StoryFactory(characters=test_characters, scenario=test_scenario)


@pytest.mark.asyncio
async def test_generate_story_success(
    authenticated_client: AsyncClient,
    test_characters,
    test_scenario,
    test_story,
):
    request_data = {
        "character_ids": [str(char.id) for char in test_characters],
        "scenario_id": str(test_scenario.id),
        "narrative_style": test_story.narrative_style,
    }

    # Act
    response = await authenticated_client.post("/stories/generate", json=request_data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert (
        response_data["title"] == f"{test_story.characters[0].name}'s Magical Adventure"
    )
    assert response_data["narrative_style"] == test_story.narrative_style
    assert response_data["scenario"]["name"] == test_scenario.name
    assert response_data["characters"][0]["name"] == test_characters[0].name


@pytest.mark.asyncio
async def test_generate_story_invalid_character_id(
    authenticated_client: AsyncClient,
    test_scenario,
):
    """Test generating a story with non-existent character IDs"""
    request_data = {
        "character_ids": [str(uuid4())],  # Non-existent character ID
        "scenario_id": str(test_scenario.id),
        "narrative_style": "adventure",
    }

    response = await authenticated_client.post("/stories/generate", json=request_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert (
        "At least one character is required to generate a story."
        == response.json()["detail"]
    )


@pytest.mark.asyncio
async def test_generate_story_multiple_characters(
    authenticated_client: AsyncClient,
    async_db_session: AsyncSession,
):
    """Test generating a story with multiple characters"""
    # Create multiple characters
    characters = [CharacterFactory() for _ in range(3)]
    for character in characters:
        async_db_session.add(CharacterModel(**character.dict()))

    # Create scenario
    scenario = ScenarioFactory()
    async_db_session.add(ScenarioModel(**scenario.dict()))
    await async_db_session.commit()

    request_data = {
        "character_ids": [str(char.id) for char in characters],
        "scenario_id": str(scenario.id),
        "narrative_style": "adventure",
    }

    response = await authenticated_client.post("/stories/generate", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert len(response_data["characters"]) == 3


@pytest.mark.asyncio
async def test_generate_story_invalid_scenario_id(
    authenticated_client: AsyncClient,
    test_characters,
):
    """Test generating a story with non-existent scenario ID"""
    request_data = {
        "character_ids": [str(char.id) for char in test_characters],
        "scenario_id": str(uuid4()),  # Non-existent scenario ID
        "narrative_style": "adventure",
    }

    response = await authenticated_client.post("/stories/generate", json=request_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Scenario not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_generate_story_invalid_narrative_style(
    authenticated_client: AsyncClient,
    test_characters,
    test_scenario,
):
    """Test generating a story with invalid narrative style"""
    request_data = {
        "character_ids": [str(char.id) for char in test_characters],
        "scenario_id": str(test_scenario.id),
        "narrative_style": "",  # Empty narrative style
    }

    response = await authenticated_client.post("/stories/generate", json=request_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
