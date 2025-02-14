import os

import requests


class LlamaClient:
    """Client for interacting with a locally hosted LLaMA API."""

    def __init__(self, model: str | None = None, api_url: str | None = None):
        self.model = model or os.getenv("LLM_MODEL", "llama3")
        self.api_url = api_url or os.getenv(
            "LLAMA_API_URL", "http://localhost:11434/v1/completions"
        )

    def generate_text(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000
    ) -> str:
        """
        Generates text using a LLaMA-based model.

        Parameters:
        ----------
        prompt : str
            The prompt text to generate the story.
        temperature : float
            Controls randomness (0 = deterministic, 1 = highly random).
        max_tokens : int
            Maximum number of tokens to generate.

        Returns:
        -------
        str
            Generated text.
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()

        return response.json().get("choices", [{}])[0].get("text", "").strip()
