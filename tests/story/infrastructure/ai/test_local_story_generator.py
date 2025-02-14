import pytest

from app.story.infrastructure.ai.local_story_generator import LocalStoryGenerator


@pytest.fixture
def local_story_generator():
    return LocalStoryGenerator()


def test_generate_story_contains_expected_content(
    local_story_generator, main_character, test_scenario
):
    # Arrange
    characters = [main_character]
    narrative_style = "whimsical"

    # Act
    story = local_story_generator.generate(characters, test_scenario, narrative_style)

    # Assert
    expected_content = (
        f"One day in {test_scenario.name}, {main_character.name} and their friends "
        "embarked on an exciting whimsical adventure."
    ).strip()
    actual_content = " ".join(story.content.split())  # Normalize whitespace

    assert actual_content == expected_content


def test_generate_story_with_multiple_characters(
    local_story_generator, main_character, supporting_character, test_scenario
):
    # Arrange
    characters = [main_character, supporting_character]
    narrative_style = "whimsical"

    # Act
    story = local_story_generator.generate(characters, test_scenario, narrative_style)

    # Assert
    assert len(story.characters) == 2
    assert story.title == f"{main_character.name}'s Magical Adventure"


def test_generate_story_with_empty_character_list_raises_error(
    local_story_generator, test_scenario
):
    # Arrange
    characters = []
    narrative_style = "whimsical"

    # Act & Assert
    with pytest.raises(IndexError):
        local_story_generator.generate(characters, test_scenario, narrative_style)
