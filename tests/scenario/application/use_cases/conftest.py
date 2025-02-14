import pytest

from tests.utils.mocks import (
    MockCharacterRepository,
    MockScenarioRepository,
    MockStoryGenerator,
)


@pytest.fixture
def mock_scenario_repository():
    return MockScenarioRepository()


@pytest.fixture
def mock_character_repository():
    return MockCharacterRepository()


@pytest.fixture
def mock_story_generator():
    return MockStoryGenerator()
