import pytest

from tests.utils.mocks import MockScenarioRepository


@pytest.fixture
def mock_scenario_repository():
    return MockScenarioRepository()
