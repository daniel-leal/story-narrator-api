import os
from unittest.mock import Mock, patch

import pytest
from requests import HTTPError

from app.core.infrastructure.ai.clients.llama_client import LlamaClient


@pytest.fixture
def llama_client():
    """Create a LlamaClient instance for testing."""
    return LlamaClient()


def test_llama_client_initialization_with_defaults(llama_client):
    assert llama_client.model == "llama3"
    assert llama_client.api_url == "http://localhost:11434/v1/completions"


def test_llama_client_initialization_with_custom_values():
    custom_model = "custom-model"
    custom_url = "http://custom-url"
    client = LlamaClient(model=custom_model, api_url=custom_url)

    assert client.model == custom_model
    assert client.api_url == custom_url


def test_llama_client_initialization_with_env_variables():
    with patch.dict(
        os.environ, {"LLM_MODEL": "env-model", "LLAMA_API_URL": "http://env-url"}
    ):
        client = LlamaClient()
        assert client.model == "env-model"
        assert client.api_url == "http://env-url"


@pytest.mark.parametrize(
    "response_json,expected_output",
    [
        ({"choices": [{"text": " Generated text"}]}, "Generated text"),
    ],
)
def test_generate_text_success(response_json, expected_output, llama_client):
    mock_response = Mock()
    mock_response.json.return_value = response_json
    mock_response.raise_for_status.return_value = None  # Make sure this line is present

    with patch("requests.post", return_value=mock_response):
        result = llama_client.generate_text(
            prompt="Test prompt", temperature=0.7, max_tokens=1000
        )
        assert result == expected_output


def test_generate_text_request_payload(llama_client):
    mock_response = Mock()
    mock_response.json.return_value = {"choices": [{"text": "Generated text"}]}

    with patch("requests.post", return_value=mock_response) as mock_post:
        prompt = "Test prompt"
        temperature = 0.5
        max_tokens = 500

        llama_client.generate_text(
            prompt=prompt, temperature=temperature, max_tokens=max_tokens
        )

        expected_payload = {
            "model": llama_client.model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        mock_post.assert_called_once_with(llama_client.api_url, json=expected_payload)


def test_generate_text_request_exception(llama_client):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = HTTPError("500 Server Error")

    with patch("requests.post", return_value=mock_response):
        with pytest.raises(HTTPError):
            llama_client.generate_text("Test prompt")
