from unittest.mock import patch

import pytest

from app.story.infrastructure.ai.chatgpt_story_generator import ChatGPTStoryGenerator


@pytest.fixture
def chatgpt_story_generator(mock_openai_client):
    return ChatGPTStoryGenerator()


def test_chatgpt_initialization_with_custom_model():
    # Arrange & Act
    with patch(
        "app.story.infrastructure.ai.chatgpt_story_generator.OpenAIClient"
    ) as mock:
        ChatGPTStoryGenerator(model="gpt-3.5-turbo")

    # Assert
    mock.assert_called_once_with(model="gpt-3.5-turbo")


def test_generate_story_returns_story_object(
    chatgpt_story_generator, main_character, test_scenario
):
    # Arrange
    characters = [main_character]
    narrative_style = "magical"

    # Act
    story = chatgpt_story_generator.generate(characters, test_scenario, narrative_style)

    # Assert
    assert story.title == f"The Adventures of {main_character.name}"
    assert story.content == "Generated story text"
    assert story.characters == characters
    assert story.scenario == test_scenario
    assert story.narrative_style == narrative_style


def test_create_prompt_with_single_character(
    chatgpt_story_generator, main_character, test_scenario
):
    # Arrange
    characters = [main_character]
    narrative_style = "magical"

    # Act
    prompt = chatgpt_story_generator._create_prompt(
        characters, test_scenario, narrative_style
    )

    # Assert
    expected_prompt = f"""
        You are an expert children's story writer. Write a {narrative_style}
        story for kids aged 3-8.

        Main Character: {main_character.name},
        Favorite Color: {main_character.favorite_color},
        Animal Friend: {main_character.animal_friend},
        Superpower: {main_character.superpower},
        Hobby: {main_character.hobby},
        Personality: {main_character.personality}.

        Other Characters: none.

        Setting: {test_scenario.name} - {test_scenario.description}

        Make it engaging, fun, and suitable for young children.
        Use simple words and short sentences.
        """
    assert prompt.strip() == expected_prompt.strip()


def test_create_prompt_with_multiple_characters(
    chatgpt_story_generator, main_character, supporting_character, test_scenario
):
    # Arrange
    characters = [main_character, supporting_character]
    narrative_style = "magical"

    # Act
    prompt = chatgpt_story_generator._create_prompt(
        characters, test_scenario, narrative_style
    )

    # Assert
    expected_prompt = f"""
        You are an expert children's story writer. Write a {narrative_style}
        story for kids aged 3-8.

        Main Character: {main_character.name},
        Favorite Color: {main_character.favorite_color},
        Animal Friend: {main_character.animal_friend},
        Superpower: {main_character.superpower},
        Hobby: {main_character.hobby},
        Personality: {main_character.personality}.

        Other Characters: {supporting_character.name}.

        Setting: {test_scenario.name} - {test_scenario.description}

        Make it engaging, fun, and suitable for young children.
        Use simple words and short sentences.
        """
    assert prompt.strip() == expected_prompt.strip()


def test_openai_client_called_with_correct_parameters(
    chatgpt_story_generator, mock_openai_client, main_character, test_scenario
):
    # Arrange
    characters = [main_character]
    narrative_style = "magical"
    expected_prompt = chatgpt_story_generator._create_prompt(
        characters, test_scenario, narrative_style
    )

    # Act
    chatgpt_story_generator.generate(characters, test_scenario, narrative_style)

    # Assert
    mock_openai_client.generate_text.assert_called_once_with(expected_prompt)


def test_generate_story_with_empty_character_list_raises_error(
    chatgpt_story_generator, test_scenario
):
    # Arrange
    characters = []
    narrative_style = "magical"

    # Act & Assert
    with pytest.raises(IndexError):
        chatgpt_story_generator.generate(characters, test_scenario, narrative_style)


def test_generate_story_preserves_input_parameters(
    chatgpt_story_generator, main_character, supporting_character, test_scenario
):
    # Arrange
    characters = [main_character, supporting_character]
    narrative_style = "magical"

    # Act
    story = chatgpt_story_generator.generate(characters, test_scenario, narrative_style)

    # Assert
    assert story.characters == characters
    assert len(story.characters) == 2
    assert story.scenario == test_scenario
    assert story.narrative_style == narrative_style
