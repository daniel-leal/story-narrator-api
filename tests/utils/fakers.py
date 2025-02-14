from factory import Factory, Faker, List, SubFactory

from app.auth.domain.entities.user import User
from app.character.domain.entities.character import Character
from app.scenario.domain.entities.scenario import Scenario
from app.story.domain.entities.story import Story


class UserFactory(Factory):
    """Factory for generating User entities."""

    class Meta:
        model = User

    id = Faker("uuid4")
    name = Faker("name")
    email = Faker("email")
    hashed_password = Faker("password")
    is_active = True


class CharacterFactory(Factory):
    """Factory for generating Character entities."""

    class Meta:
        model = Character

    id = Faker("uuid4")
    name = Faker("name")
    favorite_color = Faker("color")
    animal_friend = Faker("name")
    superpower = Faker(
        "random_element",
        elements=["strength", "flying", "invisibility", "telepathy", "speed"],
    )
    hobby = "Singing"
    personality = "Brave"


class ScenarioFactory(Factory):
    class Meta:
        model = Scenario

    id = Faker("uuid4")
    name = Faker(
        "random_element",
        elements=["Enhanced Forest", "Space Dream", "Ice Kingdom"],
    )
    description = "Description of scenario"
    available = True


class StoryFactory(Factory):
    class Meta:
        model = Story

    id = Faker("uuid4")
    title = Faker("sentence")
    content = Faker("paragraph")
    characters = List([SubFactory(CharacterFactory) for _ in range(2)])
    scenario = SubFactory(ScenarioFactory)
    narrative_style = Faker(
        "random_element", elements=["adventurous", "fantasy", "mistery"]
    )
