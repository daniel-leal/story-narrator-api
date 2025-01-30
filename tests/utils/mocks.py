from typing import List
from unittest.mock import AsyncMock, Mock

from app.auth.infrastructure.persistence.models.user import User
from app.character.domain.entities.character import Character
from app.story.domain.entities.scenario import Scenario


class MockUserRepository:
    """Mock for the UserRepository interface."""

    def __init__(self) -> None:
        self.get_by_email = AsyncMock()
        self.save = AsyncMock()

    def configure_get_by_email(self, user: User | None):
        """
        Configure the return value of the `get_by_email` method.

        Parameters
        ----------
        user : User | None
            The user to be returned when `get_by_email` is called.
        """
        self.get_by_email.return_value = user


class MockAuthService:
    """Mock for the AuthService class."""

    def __init__(self) -> None:
        self.user_repository = Mock()
        self.user_repository.get_by_email = AsyncMock()
        self.verify_password = Mock()
        self.create_access_token = Mock()
        self.register_user = AsyncMock()

    def configure_register_user(self, user: User):
        """
        Configure the return value of the `register_user` method.

        Parameters
        ----------
        user : User
            The user to be returned when `register_user` is called.
        """
        self.register_user.return_value = user

    def configure_get_by_email(self, user: User | None):
        """
        Configure the return value of the `get_by_email` method via the UserRepository.

        Parameters
        ----------
        user : User | None
            The user to be returned when `get_by_email` is called.
        """
        self.user_repository.get_by_email.return_value = user


class MockCharacterRepository:
    """Mock for the UserRepository interface."""

    def __init__(self) -> None:
        self.save = AsyncMock()

    def configure_save(self, character: Character | None):
        """
        Configures the mock save method to return the specified character.

        Parameters
        ----------
        character : Character or None
            The character object to be returned by the save method. If None, the save
            method will return None.
        """
        self.save.return_value = character


class MockScenarioRepository:
    """Mock for the ScenarioRepository interface"""

    def __init__(self) -> None:
        self.get_all = AsyncMock()
        self.get_by_id = AsyncMock()

    def configure_get_all(self, scenarios: List[Scenario] | None):
        """
        Configures the mock get_all method to return the specified scenarios.

        Parameters
        ----------
        scenarios : List[Scenario] or None
            The list of scenarios of story
        """
        self.get_all.return_value = scenarios

    def configure_get_by_id(self, scenario: Scenario | None):
        """
        Configures the mock to return a specific scenario when get_by_id is called.

        Parameters
        ----------
        scenario : Scenario or None
            The scenario to be returned by the get_by_id method. If None, get_by_id will return None.
        """
        self.get_by_id.return_value = scenario
