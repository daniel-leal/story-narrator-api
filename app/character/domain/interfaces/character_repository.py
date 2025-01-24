from abc import ABC, abstractmethod
from uuid import UUID

from app.character.domain.entities.character import Character as CharacterEntity


class BaseCharacterRepository(ABC):
    """Base character repository interface"""

    @abstractmethod
    async def save(self, character: CharacterEntity) -> CharacterEntity:
        """
        Save a character entity to the repository.
        Parameters
        ----------
        character : CharacterEntity
            The character entity to be saved.
        Returns
        -------
        CharacterEntity
            The saved character entity.
        """

    @abstractmethod
    async def get_by_id(self, character_id: UUID) -> CharacterEntity | None:
        """
        Retrieve a character entity by its unique identifier.

        Parameters
        ----------
        character_id : UUID
            The unique identifier of the character to retrieve.

        Returns
        -------
        CharacterEntity or None
            The character entity if found, otherwise None.
        """
