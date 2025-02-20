import os
from enum import Enum
from functools import lru_cache
from typing import no_type_check

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    DOCKER = "docker"


class BaseSettingsConfig(BaseSettings):
    APP_NAME: str = "Story Narrator"
    APP_VERSION: str = "1.0.0"
    ENV: str = "development"
    DEBUG: bool = False

    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "story_narrator"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"

    # JWT settings
    JWT_SECRET_KEY: str = "your_jwt_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Story Generator settings
    STORY_GENERATOR: str = "default_generator"

    # AI
    OPENAI_API_KEY: str = "your_openai_api_key"
    LLAMA_API_URL: str = "http://localhost:8000"
    LLM_MODEL: str = "default_model"

    def get_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class DevelopmentSettings(BaseSettingsConfig):
    DEBUG: bool = True


class TestingSettings(BaseSettingsConfig):
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env.test", env_file_encoding="utf-8")


class DockerSettings(BaseSettingsConfig):
    model_config = SettingsConfigDict(env_file=".env.docker", env_file_encoding="utf-8")


@no_type_check
@lru_cache()
def load_environment(env: str = "development") -> BaseSettingsConfig:
    """
    Load settings based on the environment value

    Parameters
    ----------
    env: str
        Environment value (e.g., "development", "testing", "docker")

    Returns
    -------
    BaseSettingsConfig
        class of environment variables
    """
    if env == EnvironmentType.DEVELOPMENT:
        return DevelopmentSettings()
    elif env == EnvironmentType.TESTING:
        return TestingSettings()
    elif env == EnvironmentType.DOCKER:
        return DockerSettings()
    else:
        raise ValueError(f"Unknown environment type: {env}")


env = os.environ.get("ENV", "development")
settings = load_environment(env)
