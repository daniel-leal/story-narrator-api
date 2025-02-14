from typing import List

from app.character.domain.entities.character import Character
from app.scenario.domain.entities.scenario import Scenario
from app.story.domain.entities.story import Story
from app.story.domain.interfaces.story_generator import BaseStoryGenerator


class LocalStoryGenerator(BaseStoryGenerator):
    """A simple story generator returning a fixed predefined story."""

    def generate(
        self, characters: List[Character], scenario: Scenario, narrative_style: str
    ) -> Story:
        """
        Parameters
        ----------
        characters : List[Character]
            A list of characters involved in the story.
        scenario : Scenario
            The scenario or setting where the story takes place.
        narrative_style : str
            The style in which the story is narrated.

        Returns
        -------
        Story
            The generated story object containing the title, content, characters,
            scenario, and narrative style.
        """

        content = f"""
        One day in {scenario.name}, {characters[0].name} and their friends
        embarked on an exciting {narrative_style} adventure.
        """

        return Story(
            title=f"{characters[0].name}'s Magical Adventure",
            content=content.strip(),
            characters=characters,
            scenario=scenario,
            narrative_style=narrative_style,
        )
