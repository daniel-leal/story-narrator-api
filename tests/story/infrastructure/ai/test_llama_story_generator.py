import pytest

from app.story.infrastructure.ai.llama_story_generator import LlamaStoryGenerator


@pytest.fixture
def llama_story_generator(mock_llama_client):
    return LlamaStoryGenerator()


def test_generate_story_returns_story_object(
    llama_story_generator, main_character, test_scenario
):
    # Arrange
    characters = [main_character]
    narrative_style = "whimsical"

    # Act
    story = llama_story_generator.generate(characters, test_scenario, narrative_style)

    # Assert
    assert story.title == f"The Journey of {main_character.name}"
    assert story.content == "Generated story text"
    assert story.characters == characters
    assert story.scenario == test_scenario
    assert story.narrative_style == narrative_style


def test_create_prompt_with_single_character(
    llama_story_generator, main_character, test_scenario
):
    # Arrange
    narrative_style = "whimsical"

    # Act
    prompt = llama_story_generator._create_prompt(
        main_character, [], test_scenario, narrative_style
    )

    # Assert
    expected_prompt = (
        f"Write a {narrative_style} story for kids aged 3-8 featuring {main_character.name}."
        f"{main_character.name} loves {main_character.favorite_color}, has an animal friend {main_character.animal_friend}, "
        f"and has the superpower of {main_character.superpower}. Their favorite hobby is {main_character.hobby}. "
        f"They are {main_character.personality}. "
        f"The story takes place in {test_scenario.name}, described as {test_scenario.description}. "
        f"Make it in portuguese language, fun, religious, educative (telling about God), engaging, "
        f"child-friendly, with a happy ending and a teaching moral!"
    )
    assert prompt == expected_prompt


def test_create_prompt_with_multiple_characters(
    llama_story_generator, main_character, supporting_character, test_scenario
):
    # Arrange
    narrative_style = "whimsical"
    supporting_characters = [supporting_character]

    # Act
    prompt = llama_story_generator._create_prompt(
        main_character, supporting_characters, test_scenario, narrative_style
    )

    # Assert
    expected_prompt = (
        f"Write a {narrative_style} story for kids aged 3-8 featuring {main_character.name}."
        f"{main_character.name} loves {main_character.favorite_color}, has an animal friend {main_character.animal_friend}, "
        f"and has the superpower of {main_character.superpower}. Their favorite hobby is {main_character.hobby}. "
        f"They are {main_character.personality}. They are joined by "
        f"{supporting_character.name} (a {supporting_character.personality} friend with {supporting_character.superpower}). "
        f"The story takes place in {test_scenario.name}, described as {test_scenario.description}. "
        f"Make it in portuguese language, fun, religious, educative (telling about God), engaging, "
        f"child-friendly, with a happy ending and a teaching moral!"
    )
    assert prompt == expected_prompt


def test_llama_client_called_with_correct_parameters(
    llama_story_generator, mock_llama_client, main_character, test_scenario
):
    # Arrange
    characters = [main_character]
    narrative_style = "whimsical"
    expected_prompt = llama_story_generator._create_prompt(
        main_character, [], test_scenario, narrative_style
    )

    # Act
    llama_story_generator.generate(characters, test_scenario, narrative_style)

    # Assert
    mock_llama_client.generate_text.assert_called_once_with(
        expected_prompt, max_tokens=1000, temperature=0.5
    )


def test_generate_story_with_empty_character_list_raises_error(
    llama_story_generator, test_scenario
):
    # Arrange
    characters = []
    narrative_style = "whimsical"

    # Act & Assert
    with pytest.raises(IndexError):
        llama_story_generator.generate(characters, test_scenario, narrative_style)


def test_generate_story_preserves_input_parameters(
    llama_story_generator, main_character, supporting_character, test_scenario
):
    # Arrange
    characters = [main_character, supporting_character]
    narrative_style = "whimsical"

    # Act
    story = llama_story_generator.generate(characters, test_scenario, narrative_style)

    # Assert
    assert story.characters == characters
    assert len(story.characters) == 2
    assert story.scenario == test_scenario
    assert story.narrative_style == narrative_style
