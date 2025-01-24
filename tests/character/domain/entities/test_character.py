from uuid import UUID

from app.character.domain.entities.character import Character


def test_character_creation():
    character = Character(name="Alice")
    assert character.name == "Alice"
    assert isinstance(character.id, UUID)
    assert character.favorite_color is None
    assert character.animal_friend is None
    assert character.superpower is None
    assert character.hobby is None
    assert character.personality is None


def test_character_with_optional_fields():
    character = Character(
        name="Bob",
        favorite_color="Blue",
        animal_friend="Dog",
        superpower="Invisibility",
        hobby="Reading",
        personality="Cheerful",
    )
    assert character.name == "Bob"
    assert character.favorite_color == "Blue"
    assert character.animal_friend == "Dog"
    assert character.superpower == "Invisibility"
    assert character.hobby == "Reading"
    assert character.personality == "Cheerful"


def test_character_partial_optional_fields():
    character = Character(name="Charlie", favorite_color="Green", hobby="Swimming")
    assert character.name == "Charlie"
    assert character.favorite_color == "Green"
    assert character.animal_friend is None
    assert character.superpower is None
    assert character.hobby == "Swimming"
    assert character.personality is None


def test_character_id_generation():
    character1 = Character(name="Dave")
    character2 = Character(name="Eve")
    assert character1.id != character2.id
    character2 = Character(name="Eve")
    assert character1.id != character2.id
