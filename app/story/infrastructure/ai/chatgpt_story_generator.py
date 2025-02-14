from typing import List

from app.character.domain.entities.character import Character
from app.core.infrastructure.ai.clients.openai_client import OpenAIClient
from app.scenario.domain.entities.scenario import Scenario
from app.story.domain.entities.story import Story
from app.story.domain.interfaces.story_generator import BaseStoryGenerator


class ChatGPTStoryGenerator(BaseStoryGenerator):
    """Story generator using OpenAI's ChatGPT API."""

    def __init__(self, model: str = "gpt-4"):
        """
        Initializes the ChatGPT-based story generator.

        Parameters
        ----------
        model : str
            The OpenAI model to use (default: "gpt-4").
        """
        self.openai_client = OpenAIClient(model=model)

    def generate(
        self, characters: List[Character], scenario: Scenario, narrative_style: str
    ) -> Story:
        """
        Generate a story using OpenAI's ChatGPT.

        Parameters
        ----------
        characters : List[Character]
            A list of characters in the story (first character is the main protagonist).
        scenario : Scenario
            The setting for the story.
        narrative_style : str
            The storytelling style (e.g., adventurous, comedy, mystery).

        Returns
        -------
        Story
            The generated story object.
        """

        prompt = self._create_prompt(characters, scenario, narrative_style)
        story_text = self.openai_client.generate_text(prompt)
        main_character = characters[0].name

        return Story(
            title=f"The Adventures of {main_character}",
            content=story_text,
            characters=characters,
            scenario=scenario,
            narrative_style=narrative_style,
        )

    def _create_prompt(
        self, characters: List[Character], scenario: Scenario, narrative_style: str
    ) -> str:
        """
        Generates a detailed prompt for OpenAI.

        Parameters
        ----------
        characters : List[Character]
            List of characters.
        scenario : Scenario
            The setting for the story.
        narrative_style : str
            The storytelling style.

        Returns
        -------
        str
            The formatted prompt for the AI model.
        """

        main_character = characters[0]
        other_characters = (
            ", ".join([char.name for char in characters[1:]])
            if len(characters) > 1
            else "none"
        )

        return f"""
        You are an expert children's story writer. Write a {narrative_style}
        story for kids aged 3-8.

        Main Character: {main_character.name},
        Favorite Color: {main_character.favorite_color},
        Animal Friend: {main_character.animal_friend},
        Superpower: {main_character.superpower},
        Hobby: {main_character.hobby},
        Personality: {main_character.personality}.

        Other Characters: {other_characters}.

        Setting: {scenario.name} - {scenario.description}

        Make it engaging, fun, and suitable for young children.
        Use simple words and short sentences.
        """
