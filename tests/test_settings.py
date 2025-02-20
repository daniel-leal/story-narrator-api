import os

import pytest

from app.core.settings.config import (
    DevelopmentSettings,
    DockerSettings,
    TestingSettings,
    load_environment,
)


@pytest.fixture(autouse=True)
def set_env():
    original_env = os.environ.get("ENV")
    yield
    if original_env is not None:
        os.environ["ENV"] = original_env
    else:
        del os.environ["ENV"]


def test_load_development_settings():
    env = "development"
    os.environ["ENV"] = env

    settings = load_environment(env)

    assert isinstance(settings, DevelopmentSettings)
    assert settings.DEBUG is True
    assert settings.APP_NAME == "story-narrator"


def test_load_testing_settings():
    env = "testing"
    os.environ["ENV"] = env

    settings = load_environment(env)

    assert isinstance(settings, TestingSettings)
    assert settings.DB_NAME == "story_narrator_test"


def test_load_docker_settings():
    env = "docker"
    os.environ["ENV"] = env

    settings = load_environment(env)

    assert isinstance(settings, DockerSettings)
    assert settings.DB_HOST == "db"


def test_invalid_environment():
    os.environ["ENV"] = "invalid_env"

    with pytest.raises(ValueError):
        load_environment("invalid_env")


def test_database_url():
    os.environ["ENV"] = "development"
    settings = load_environment()
    expected_url = (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    assert settings.get_database_url() == expected_url
