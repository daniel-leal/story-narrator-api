from app.character.domain.entities.character import Character
from app.character.domain.interfaces.character_repository import BaseCharacterRepository


class CreateCharacterUseCase:
    """Use case for creating a character"""

    def __init__(self, character_repository: BaseCharacterRepository) -> None:
        self.character_repository = character_repository

    async def execute(
        self,
        name: str,
        favorite_color: str | None,
        animal_friend: str | None,
        superpower: str | None,
        hobby: str | None,
        personality: str | None,
    ) -> Character:
        """
        Creates a new character with the provided attributes and saves it to the repository.

        Parameters
        ----------
        name : str
            The name of the character.
        favorite_color : str
            The favorite color of the character.
        animal_friend : str
            The animal friend of the character.
        superpower : str
            The superpower of the character.
        hobby : str
            The hobby of the character.
        personality : str
            The personality of the character.

        Returns
        -------
        Character
            The created character object.
        """
        character = Character(
            name=name,
            favorite_color=favorite_color,
            animal_friend=animal_friend,
            superpower=superpower,
            hobby=hobby,
            personality=personality,
        )
        return await self.character_repository.save(character)
