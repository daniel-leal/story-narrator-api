from typing import Final, List, Tuple
from uuid import UUID

from app.character.domain.entities.character import Character
from app.character.domain.interfaces.character_repository import BaseCharacterRepository
from app.scenario.domain.entities.scenario import Scenario
from app.scenario.domain.interfaces.scenario_repository import BaseScenarioRepository
from app.story.domain.entities.story import Story
from app.story.domain.exceptions.story_exceptions import (
    CharactersEmptyError,
    InvalidNarrativeStyleError,
    InvalidScenarioError,
    TooManyCharactersError,
)
from app.story.domain.interfaces.story_generator import BaseStoryGenerator


class GenerateStoryUseCase:
    """Use case for generating a story based on characters, scenario, and narrative style."""

    MAX_CHARACTERS: Final[int] = 5

    def __init__(
        self,
        story_generator: BaseStoryGenerator,
        character_repository: BaseCharacterRepository,
        scenario_repository: BaseScenarioRepository,
    ) -> None:
        """
        Initializes the use case with repositories and a story generator.

        Parameters:
        ----------
        story_generator : BaseStoryGenerator
            The AI-based story generator (e.g., ChatGPT, Llama, Local).
        character_repository : BaseCharacterRepository
            The repository to fetch characters.
        scenario_repository : BaseScenarioRepository
            The repository to fetch scenarios.
        """
        self.story_generator = story_generator
        self.character_repository = character_repository
        self.scenario_repository = scenario_repository

    async def execute(
        self, character_ids: List[UUID], scenario_id: UUID, narrative_style: str
    ) -> Story:
        """
        Generates a story using the provided character IDs, scenario ID, and narrative style.

        Parameters
        ----------
        character_ids : List[UUID]
            The list of character UUIDs.
        scenario_id : UUID
            The UUID of the scenario.
        narrative_style : str
            The storytelling style (e.g., adventurous, comedy, mystery).

        Returns
        -------
        Story
            The generated story object.
        """

        characters = [
            char
            for cid in character_ids
            if (char := await self.character_repository.get_by_id(cid)) is not None
        ]

        _, scenario, _ = await self._validate(characters, scenario_id, narrative_style)

        return self.story_generator.generate(characters, scenario, narrative_style)

    async def _validate(
        self,
        characters: List[Character],
        scenario_id: UUID,
        narrative_style: str,
    ) -> Tuple[List[Character], Scenario, str]:
        """
        Validates the input parameters for story generation.

        Parameters
        ----------
        characters : List[Character] or optional
            The list of characters.
        scenario_id : UUID
            The ID of the selected story scenario.
        narrative_style : str
            The chosen narrative style.

        Returns
        -------
        Tuple[List[Character], Scenario, str]
            A tuple containing the validated characters, scenario, and narrative style.

        Raises
        ------
        StoryValidationError
            If any validation rule is not met.
        """
        if not characters:
            raise CharactersEmptyError()

        if len(characters) > self.MAX_CHARACTERS:
            raise TooManyCharactersError(self.MAX_CHARACTERS)

        scenario = await self.scenario_repository.get_by_id(scenario_id)
        if not scenario:
            raise InvalidScenarioError()

        if not isinstance(narrative_style, str) or not narrative_style.strip():
            raise InvalidNarrativeStyleError()

        return characters, scenario, narrative_style
