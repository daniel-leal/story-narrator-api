import os
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.auth.domain.entities.user import User
from app.auth.domain.exceptions.user_exceptions import UserAlreadyRegisteredError
from app.auth.domain.interfaces.user_repository import BaseUserRepository


class AuthService:
    """Service to handle authentication and authorization."""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_repository: BaseUserRepository) -> None:
        self.user_repository = user_repository
        self.secret_key = os.getenv("JWT_SECRET_KEY", "default_secret")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30)
        )

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
            minutes=self.access_token_expire_minutes
        )
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": expire,
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict:
        """
        Verify and decode a JWT token.

        Parameters
        ----------
        token : str
            JWT token to verify.

        Returns
        -------
        dict
            Decoded token payload.

        Raises
        ------
        JWTError
            If token is invalid or expired.
        """
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
