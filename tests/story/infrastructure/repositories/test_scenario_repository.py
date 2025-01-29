from typing import List

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.story.domain.entities.scenario import Scenario as ScenarioEntity
from app.story.infrastructure.persistence.models.scenario import (
    Scenario as ScenarioModel,
)
from app.story.infrastructure.repositories.scenario_repository import ScenarioRepository
from tests.utils.fakers import ScenarioFactory


@pytest.mark.asyncio
async def test_get_all_with_no_data(async_db_session: AsyncSession):
    # Arrange
    scenario_repository = ScenarioRepository(async_db_session)

    # Act
    response = await scenario_repository.get_all()

    # Assert
    assert response == []


@pytest.mark.asyncio
async def test_get_all_with_data(async_db_session: AsyncSession):
    # Arrange
    scenario_repository = ScenarioRepository(async_db_session)
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
