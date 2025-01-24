from fastapi import HTTPException

from app.auth.domain.services.auth_service import AuthService


class LoginUserUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def execute(self, email: str, password: str) -> str:
        """
        Handles user login, including verifying credentials and generating JWT tokens.

        Parameters
        ----------
        email : str
            User's email.
        password : str
            User's password.

        Returns
        -------
        str
            JWT token.
        """
        user = await self.auth_service.user_repository.get_by_email(email)

        if not user or not self.auth_service.verify_password(
            password, user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not user.is_active:
            raise HTTPException(status_code=401, detail="Inactive user")

        return self.auth_service.create_access_token(user)
