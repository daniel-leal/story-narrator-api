from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.character.domain.entities.character import Character as CharacterEntity
from app.character.domain.interfaces.character_repository import BaseCharacterRepository
from app.character.infrastructure.persistence.models.character import (
    Character as CharacterModel,
)


class CharacterRepository(BaseCharacterRepository):
    """Implementation of character repository"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, character: CharacterEntity) -> CharacterEntity:
        """
        Asynchronously saves a CharacterEntity to the database.
        Parameters
        ----------
        character : CharacterEntity
            The character entity to be saved.
        Returns
        -------
        CharacterEntity
            The saved character entity with updated attributes from the database.
        """

        character_model = CharacterModel(
            id=character.id,
            name=character.name,
            favorite_color=character.favorite_color,
            animal_friend=character.animal_friend,
            superpower=character.superpower,
            hobby=character.hobby,
            personality=character.personality,
        )

        self.session.add(character_model)
        await self.session.commit()
        await self.session.refresh(character_model)

        return CharacterEntity(**character_model.__dict__)

    async def get_by_id(self, character_id: UUID) -> CharacterEntity | None:
        """
        Asynchronously retrieve a character entity by its ID.
        Parameters
        ----------
        character_id : UUID
            The unique identifier of the character to retrieve.
        Returns
        -------
        CharacterEntity or None
            The character entity if found, otherwise None.
        """

        result = await self.session.execute(
            select(CharacterModel).filter_by(id=character_id)
        )

        character_model = result.scalar_one_or_none()

        if character_model:
            return CharacterEntity(**character_model.__dict__)

        return None
