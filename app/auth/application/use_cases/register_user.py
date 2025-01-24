import logging

from app.auth.domain.entities.user import User
from app.auth.domain.services.auth_service import AuthService

logger = logging.getLogger(__name__)


class RegisterUserUseCase:
    def __init__(self, auth_service: AuthService) -> None:
        self.auth_service = auth_service

    async def execute(self, name: str, email: str, password: str) -> User:
        """
        Handle the user registration, including input validation and invoking the domain
        service.

        Parameters
        ----------
        name : str
            User's name.
        email : str
            User's email.
        password : str
            User's password.

        Returns
        -------
        User
            The registered user.
        """
        logger.info(f"Registering user: name={name}, email={email}")
        user = await self.auth_service.register_user(name, email, password)
        logger.info(f"User registered: name={user.name}, email={user.email}")
        return user
