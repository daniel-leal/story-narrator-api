import logging
import os

from openai import OpenAI, OpenAIError

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client for interacting with OpenAI's API."""

    def __init__(self, model: str | None = None, api_key: str | None = None):
        """
        Initializes the OpenAI client.

        Parameters
        ----------
        model : str
            The OpenAI model to use (default: "gpt-4").
        api_key : Optional[str]
            The API key for OpenAI (defaults to environment variable).
        """
        self.model = model or os.getenv("LLM_MODEL", "gpt-4")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                """OpenAI API key is missing. Set OPENAI_API_KEY in .env or pass it
                explicitly."""
            )

        self.client = OpenAI(api_key=self.api_key)

    def generate_text(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 500
    ) -> str:
        """
        Generates text from OpenAI's API.

        Parameters
        ----------
        prompt : str
            The prompt text to generate the story.
        temperature : float
            Controls randomness (0 = deterministic, 1 = highly random).
        max_tokens : int
            Maximum number of tokens to generate.

        Returns
        -------
        str
            Generated text.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content
            if not content:
                return "A story with openai could not be generated."

            return content.strip()

        except OpenAIError as e:
            logger.error(f"OpenAI API Error: {e}")
            return "An error occurred while generating the story."
