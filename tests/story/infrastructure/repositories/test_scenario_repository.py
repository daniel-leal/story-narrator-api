from typing import List
from uuid import UUID

import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from app.story.domain.entities.scenario import Scenario as ScenarioEntity
from app.story.infrastructure.persistence.models.scenario import (
    Scenario as ScenarioModel,
)
from app.story.infrastructure.repositories.scenario_repository import ScenarioRepository
from tests.utils.fakers import ScenarioFactory


@pytest.fixture
def scenario_repository(async_db_session: AsyncSession) -> ScenarioRepository:
    return ScenarioRepository(async_db_session)


@pytest.fixture
def scenario_id() -> UUID:
    return UUID("123e4567-e89b-12d3-a456-426614174000")


@pytest.mark.asyncio
async def test_get_all_with_no_data(scenario_repository: ScenarioRepository):
    # Act
    response = await scenario_repository.get_all()

    # Assert
    assert response == []


@pytest.mark.asyncio
async def test_get_all_with_data(
    scenario_repository: ScenarioRepository, async_db_session: AsyncSession
):
    # Arrange
    factories: List[ScenarioEntity] = [
        ScenarioFactory.create(name="Enhance Forest"),
        ScenarioFactory.create(name="Space Dream"),
    ]
    scenarios = [
        ScenarioModel(name=scenario.name, description=scenario.description)
        for scenario in factories
    ]

    async_db_session.add_all(scenarios)
    await async_db_session.commit()

    # Act
    response = await scenario_repository.get_all()

    # Assert
    assert len(response) == 2


@pytest.mark.asyncio
async def test_get_all_with_mixed_availability(
    scenario_repository: ScenarioRepository, async_db_session: AsyncSession
):
    # Arrange
    factories: List[ScenarioEntity] = [
        ScenarioFactory.create(name="Enhance Forest", available=True),
        ScenarioFactory.create(name="Space Dream", available=False),
    ]
    scenarios = [
        ScenarioModel(
            name=scenario.name,
            description=scenario.description,
            available=scenario.available,
        )
        for scenario in factories
    ]

    async_db_session.add_all(scenarios)
    await async_db_session.commit()

    # Act
    response = await scenario_repository.get_all()

    # Assert
    assert len(response) == 1
    assert response[0].name == "Enhance Forest"


@pytest.mark.asyncio
async def test_get_by_id_with_success(
    scenario_repository: ScenarioRepository,
    async_db_session: AsyncSession,
    scenario_id: UUID,
):
    # Arrange
    factory: ScenarioEntity = ScenarioFactory.create()
    async_db_session.add(
        ScenarioModel(
            id=scenario_id, name=factory.name, description=factory.description
        )
    )
    await async_db_session.commit()

    # Act
    result = await scenario_repository.get_by_id(scenario_id)

    # Assert
    assert result is not None
    assert result.name == factory.name
    assert result.description == factory.description


@pytest.mark.asyncio
async def test_get_by_id_with_nonexistent_id(
    scenario_repository: ScenarioRepository, scenario_id: UUID
):
    # Act
    result = await scenario_repository.get_by_id(scenario_id)

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_get_by_id_with_invalid_uuid(scenario_repository: ScenarioRepository):
    # Arrange
    invalid_scenario_id = "invalid-uuid"

    # Act & Assert
    with pytest.raises(sqlalchemy.exc.DBAPIError):
        await scenario_repository.get_by_id(invalid_scenario_id)  # type: ignore


@pytest.mark.asyncio
async def test_get_by_name_with_success(
    scenario_repository: ScenarioRepository, async_db_session: AsyncSession
):
    # Arrange
    factory: ScenarioEntity = ScenarioFactory.create(name="Mystic River")
    async_db_session.add(
        ScenarioModel(name=factory.name, description=factory.description)
    )
    await async_db_session.commit()

    # Act
    result = await scenario_repository.get_by_name("Mystic River")

    # Assert
    assert result is not None
    assert result.name == factory.name
    assert result.description == factory.description


@pytest.mark.asyncio
async def test_get_by_name_with_nonexistent_name(
    scenario_repository: ScenarioRepository,
):
    # Act
    result = await scenario_repository.get_by_name("Nonexistent Scenario")

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_save_scenario(scenario_repository: ScenarioRepository):
    # Arrange
    factory: ScenarioEntity = ScenarioFactory.create(name="New Scenario")

    # Act
    saved_scenario = await scenario_repository.save(factory)
    scenario_id = saved_scenario.id

    # Assert
    assert saved_scenario is not None
    assert scenario_id is not None
    assert saved_scenario.name == factory.name
    assert saved_scenario.description == factory.description

    # Verify the scenario is actually saved in the database
    result = await scenario_repository.get_by_id(scenario_id)
    assert result is not None
    assert result.name == factory.name
    assert result.description == factory.description
