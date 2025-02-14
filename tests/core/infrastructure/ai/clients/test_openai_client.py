from unittest.mock import Mock, patch

import pytest
from openai import OpenAIError

from app.core.infrastructure.ai.clients.openai_client import OpenAIClient


@pytest.fixture
def mock_openai():
    with patch('app.core.infrastructure.ai.clients.openai_client.OpenAI') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_response():
    mock = Mock()
    mock.choices = [
        Mock(
            message=Mock(
                content="Generated story content"
            )
        )
    ]
    return mock


@pytest.fixture
def clean_env(monkeypatch):
    """Clean environment variables before each test"""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    return monkeypatch


def test_init_with_default_values(clean_env):
    # Arrange
    clean_env.setenv("OPENAI_API_KEY", "test-api-key")

    # Act
    client = OpenAIClient()

    # Assert
    assert client.model == "gpt-4"
    assert client.api_key == "test-api-key"


def test_init_with_custom_values(clean_env):
    # Arrange
    custom_model = "gpt-3.5-turbo"
    custom_api_key = "custom-api-key"

    # Act
    client = OpenAIClient(model=custom_model, api_key=custom_api_key)

    # Assert
    assert client.model == custom_model
    assert client.api_key == custom_api_key


def test_init_without_api_key(clean_env):
    # Arrange & Act & Assert
    with pytest.raises(ValueError, match="OpenAI API key is missing"):
        OpenAIClient(api_key=None)


def test_generate_text_success(mock_openai, mock_response, clean_env):
    # Arrange
    client = OpenAIClient(api_key="test-api-key")
    mock_openai.chat.completions.create.return_value = mock_response
    prompt = "Test prompt"

    # Act
    result = client.generate_text(prompt)

    # Assert
    assert result == "Generated story content"
    mock_openai.chat.completions.create.assert_called_once_with(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )


def test_generate_text_with_custom_parameters(mock_openai, mock_response, clean_env):
    # Arrange
    client = OpenAIClient(api_key="test-api-key")
    mock_openai.chat.completions.create.return_value = mock_response
    prompt = "Test prompt"
    temperature = 0.5
    max_tokens = 1000

    # Act
    result = client.generate_text(prompt, temperature=temperature, max_tokens=max_tokens)

    # Assert
    assert result == "Generated story content"
    mock_openai.chat.completions.create.assert_called_once_with(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )


def test_generate_text_empty_response(mock_openai, clean_env):
    # Arrange
    client = OpenAIClient(api_key="test-api-key")
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content=""))]
    mock_openai.chat.completions.create.return_value = mock_response

    # Act
    result = client.generate_text("Test prompt")

    # Assert
    assert result == "A story with openai could not be generated."


def test_generate_text_api_error(mock_openai, clean_env):
    # Arrange
    client = OpenAIClient(api_key="test-api-key")
    mock_openai.chat.completions.create.side_effect = OpenAIError("API Error")

    # Act
    result = client.generate_text("Test prompt")

    # Assert
    assert result == "An error occurred while generating the story."


@pytest.mark.parametrize(
    "env_model,expected_model",
    [
        ("gpt-4", "gpt-4"),
        ("gpt-3.5-turbo", "gpt-3.5-turbo"),
        (None, "gpt-4"),  # default value
    ]
)
def test_model_initialization_from_env(clean_env, env_model, expected_model):
    # Arrange
    clean_env.setenv("OPENAI_API_KEY", "test-api-key")
    if env_model:
        clean_env.setenv("LLM_MODEL", env_model)

    # Act
    client = OpenAIClient()

    # Assert
    assert client.model == expected_model


def test_generate_text_strips_whitespace(mock_openai, clean_env):
    # Arrange
    client = OpenAIClient(api_key="test-api-key")
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="  content with whitespace  "))]
    mock_openai.chat.completions.create.return_value = mock_response

    # Act
    result = client.generate_text("Test prompt")

    # Assert
    assert result == "content with whitespace"
