from app.character.domain.entities.character import Character
from app.scenario.domain.entities.scenario import Scenario
from app.story.domain.entities.story import Story


def test_story_initialization():
    title = "Test Story"
    content = "This is a test story content"
    characters = [Character(name="Test Character")]
    scenario = Scenario(name="Test Scenario", description="Test Description")
    narrative_style = "first_person"

    story = Story(
        title=title,
        content=content,
        characters=characters,
        scenario=scenario,
        narrative_style=narrative_style,
    )

    assert story.title == title
    assert story.content == content
    assert story.characters == characters
    assert story.scenario == scenario
    assert story.narrative_style == narrative_style


def test_story_with_multiple_characters():
    title = "Multiple Characters Story"
    content = "Story with multiple characters"
    characters = [
        Character(name="Character 1"),
        Character(name="Character 2"),
        Character(name="Character 3"),
    ]
    scenario = Scenario(name="Test Scenario", description="Test Description")
    narrative_style = "third_person"

    story = Story(
        title=title,
        content=content,
        characters=characters,
        scenario=scenario,
        narrative_style=narrative_style,
    )

    assert len(story.characters) == 3
    assert story.narrative_style == "third_person"
