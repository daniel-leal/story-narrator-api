from uuid import uuid4

import pytest

from app.core.dependencies import get_scenario_use_case
from tests.utils.fakers import ScenarioFactory


@pytest.mark.asyncio
async def test_get_scenario_with_invalid_id(mock_scenario_repository):
    # Arrange
    invalid_id = uuid4()
    mock_scenario_repository.configure_get_by_id(None)
    use_case = get_scenario_use_case(mock_scenario_repository)

    # Act
    result = await use_case.execute(invalid_id)

    # Assert
    assert result is None
    mock_scenario_repository.get_by_id.assert_called_once_with(invalid_id)


@pytest.mark.asyncio
async def test_get_scenario_with_valid_id(mock_scenario_repository):
    # Arrange
    scenario = ScenarioFactory.create(name="Test Scenario")
    mock_scenario_repository.configure_get_by_id(scenario)
    use_case = get_scenario_use_case(mock_scenario_repository)

    # Act
    result = await use_case.execute(scenario.id)

    # Assert
    assert result == scenario
    mock_scenario_repository.get_by_id.assert_called_once_with(scenario.id)
