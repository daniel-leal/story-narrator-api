import os
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import UserAlreadyRegisteredError
from app.domain.interfaces.user_repository import BaseUserRepository


class AuthService:
    """Service to handle authentication and authorization."""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_repository: BaseUserRepository) -> None:
        self.user_repository = user_repository

    def hash_password(self, password: str) -> str:
        """
        Hash the password.

        Parameters
        ----------
        password : str
            Plain password.

        Returns
        -------
        str
            Hashed password.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify if the plain password matches the hashed password.

        Parameters
        ----------
        plain_password : str
            Plain password.
        hashed_password : str
            Hashed password.

        Returns
        -------
        bool
            True if the passwords match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    async def register_user(self, name: str, email: str, password: str) -> User:
        """
        Register a new user.

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
            User instance.
        """
        if await self.user_repository.get_by_email(email):
            raise UserAlreadyRegisteredError(email)

        hashed_password = self.hash_password(password)
        user = User(name=name, email=email, hashed_password=hashed_password)
        await self.user_repository.save(user)
        return user

    def create_access_token(self, user: User) -> str:
        """
        Create a JWT token for the user.

        Parameters
        ----------
        user : User
            User instance.

        Returns
        -------
        str
            JWT token.
        """
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
        )
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": expire,
        }
        secret_key = os.getenv("JWT_SECRET_KEY", "default_secret")
        algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        return jwt.encode(payload, secret_key, algorithm=algorithm)
