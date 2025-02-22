import pytest

from app.core.dependencies import get_scenarios_use_case
from app.scenario.domain.entities.scenario import Scenario
from tests.utils.fakers import ScenarioFactory


@pytest.mark.asyncio
async def test_get_all_scenarios(mock_scenario_repository):
    mock_scenario_repository.configure_get_all = []

    use_case = get_scenarios_use_case(mock_scenario_repository)
    scenarios = await use_case.execute()

    assert all(isinstance(scenario, Scenario) for scenario in scenarios)
    mock_scenario_repository.get_all.assert_called_once


@pytest.mark.asyncio
async def test_get_all_scenarios_with_data(mock_scenario_repository):
    scenarios = ScenarioFactory.create_batch(3)
    mock_scenario_repository.configure_get_all(scenarios)

    use_case = get_scenarios_use_case(mock_scenario_repository)
    scenarios = await use_case.execute()

    assert len(scenarios) == 3
    mock_scenario_repository.get_all.assert_called_once
