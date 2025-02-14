from typing import List

from app.character.domain.entities.character import Character
from app.core.infrastructure.ai.clients.llama_client import LlamaClient
from app.scenario.domain.entities.scenario import Scenario
from app.story.domain.entities.story import Story
from app.story.domain.interfaces.story_generator import BaseStoryGenerator


class LlamaStoryGenerator(BaseStoryGenerator):
    """Story generator using LLaMA API."""

    def __init__(self) -> None:
        """
        Initializes the LLaMA story generator.

        Parameters
        ----------
        llama_client : LlamaClient, optional
            The client for interacting with the LLaMA API.
        """
        self.llama_client = LlamaClient()

    def generate(
        self, characters: List[Character], scenario: Scenario, narrative_style: str
    ) -> Story:
        """
        Generate a story using a LLaMA-based model.

        Parameters
        ----------
        characters: List[Character]
            List of character objects.
        scenario: Scenario
            The selected story setting.
        narrative_style: str
            The chosen narrative style.

        Returns
        -------
        Story
            A generated Story object.
        """

        main_character = characters[0]
        supporting_characters = characters[1:]

        prompt = self._create_prompt(
            main_character, supporting_characters, scenario, narrative_style
        )

        story_text = self.llama_client.generate_text(
            prompt, max_tokens=1000, temperature=0.5
        )

        return Story(
            title=f"The Journey of {characters[0].name}",
            content=story_text,
            characters=characters,
            scenario=scenario,
            narrative_style=narrative_style,
        )

    def _create_prompt(
        self,
        main_character: Character,
        supporting_characters: List[Character],
        scenario: Scenario,
        narrative_style: str,
    ) -> str:
        """
        Generates a structured prompt for the LLaMA API.

        Parameters
        ----------
        main_character : Character
            The main character of the story.
        supporting_characters : List[Character]
            List of supporting characters.
        scenario : Scenario
            The story scenario.
        narrative_style : str
            The selected narrative style.

        Returns
        -------
        str
            A structured prompt for the story generation.
        """

        supporting_text = ""
        if supporting_characters:
            supporting_text = " They are joined by "
            supporting_text += (
                ", ".join(
                    f"{char.name} (a {char.personality} friend with {char.superpower})"
                    for char in supporting_characters
                )
                + "."
            )

        return (
            f"Write a {narrative_style} story for kids aged 3-8 featuring {main_character.name}."
            f"{main_character.name} loves {main_character.favorite_color}, has an animal friend {main_character.animal_friend}, "
            f"and has the superpower of {main_character.superpower}. Their favorite hobby is {main_character.hobby}. "
            f"They are {main_character.personality}.{supporting_text} "
            f"The story takes place in {scenario.name}, described as {scenario.description}. "
            f"Make it in portuguese language, fun, religious, educative (telling about God), engaging, "
            f"child-friendly, with a happy ending and a teaching moral!"
        )
