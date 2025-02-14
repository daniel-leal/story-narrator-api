from abc import ABC, abstractmethod
from typing import List

from app.character.domain.entities.character import Character
from app.scenario.domain.entities.scenario import Scenario
from app.story.domain.entities.story import Story


class BaseStoryGenerator(ABC):
    """Abstract base class for all story generators."""

    @abstractmethod
    def generate(
        self, characters: List[Character], scenario: Scenario, narrative_style: str
    ) -> Story:
        """
        Generate a story based on given characters, scenario, and narrative style.

        Parameters
        ----------
        characters: List[Character]
            List of character names.
        scenario: Scenario
            The story setting.
        narrative_style: str
            The chosen narrative style.

        Returns
        -------
        Story: A generated Story object.
        """
