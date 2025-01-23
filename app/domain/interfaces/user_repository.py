from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.user import User


class BaseUserRepository(ABC):
    """Base user repository interface"""

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email

        Parameters
        ----------
        email : str

        Returns
        -------
        Optional[User]: User or None
        """

    @abstractmethod
    async def save(self, user: User) -> None:
        """
        Save a user

        Parameters
        ----------
        user

        Returns
        -------
        None
        """
