import pytest

from app.core.dependencies import get_create_scenario_use_case
from app.scenario.application.use_cases.create_scenario import CreateScenarioUseCase
from app.scenario.domain.entities.scenario import Scenario
from app.scenario.domain.exceptions.scenario_exceptions import (
    InvalidScenarioDataError,
    ScenarioAlreadyExistsError,
)
from tests.utils.fakers import ScenarioFactory


@pytest.fixture
def scenario() -> Scenario:
    return ScenarioFactory.create(name="Test Scenario", description="Test Description")


@pytest.mark.asyncio
async def test_create_scenario_success(mock_scenario_repository, scenario):
    # Arrange
    mock_scenario_repository.configure_get_by_name(None)
    mock_scenario_repository.configure_save(scenario)
    use_case = get_create_scenario_use_case(
        scenario_repository=mock_scenario_repository
    )

    # Act
    scenario = await use_case.execute(
        name="Test Scenario", description="Test Description"
    )

    # Assert
    assert scenario.name == "Test Scenario"
    assert scenario.description == "Test Description"
    mock_scenario_repository.get_by_name.assert_called_once_with("Test Scenario")
    mock_scenario_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_scenario_already_exists(mock_scenario_repository, scenario):
    # Arrange
    mock_scenario_repository.configure_get_by_name(scenario)
    use_case = get_create_scenario_use_case(
        scenario_repository=mock_scenario_repository
    )

    # Act & Assert
    with pytest.raises(ScenarioAlreadyExistsError):
        await use_case.execute(name="Test Scenario", description="Test Description")
    mock_scenario_repository.get_by_name.assert_called_once_with("Test Scenario")
    mock_scenario_repository.save.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, description",
    [
        ("", "Test Description"),
        ("Test Scenario", ""),
        ("T" * 101, "Test Description"),
        ("Test Scenario", "D" * 501),
    ],
)
async def test_create_scenario_invalid_data(
    mock_scenario_repository, name, description
):
    # Arrange
    use_case = CreateScenarioUseCase(scenario_repository=mock_scenario_repository)

    # Act & Assert
    with pytest.raises(InvalidScenarioDataError):
        await use_case.execute(name=name, description=description)
    mock_scenario_repository.get_by_name.assert_not_called()
    mock_scenario_repository.save.assert_not_called()
