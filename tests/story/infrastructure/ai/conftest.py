from unittest.mock import Mock, patch

import pytest

from tests.utils.fakers import CharacterFactory, ScenarioFactory


@pytest.fixture
def mock_llama_client():
    with patch('app.story.infrastructure.ai.llama_story_generator.LlamaClient') as mock:
        mock_instance = Mock()
        mock_instance.generate_text.return_value = "Generated story text"
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_openai_client():
    with patch('app.story.infrastructure.ai.chatgpt_story_generator.OpenAIClient') as mock:
        mock_instance = Mock()
        mock_instance.generate_text.return_value = "Generated story text"
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def main_character():
    return CharacterFactory(
        name="Lucy",
        favorite_color="purple",
        animal_friend="unicorn",
        superpower="magic",
        hobby="painting",
        personality="creative"
    )


@pytest.fixture
def supporting_character():
    return CharacterFactory(
        name="Tom",
        favorite_color="green",
        animal_friend="dragon",
        superpower="fire-breathing",
        hobby="dancing",
        personality="energetic"
    )


@pytest.fixture
def test_scenario():
    return ScenarioFactory(
        name="Crystal Palace",
        description="A shimmering castle made of pure crystal"
    )
