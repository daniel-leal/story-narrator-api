from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.domain.entities.user import User as UserEntity
from app.auth.domain.interfaces.user_repository import BaseUserRepository
from app.auth.infrastructure.persistence.models.user import User as UserModel


class UserRepository(BaseUserRepository):
    """Implementation of user repository"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> UserEntity | None:
        """
        Get user by email

        Parameters
        ----------
        email : str
            User email

        Returns
        -------
        UserEntity | None
            User entity if user exists, None otherwise
        """
        result = await self.session.execute(select(UserModel).filter_by(email=email))
        user = result.scalar_one_or_none()
        if user:
            return UserEntity.model_validate(user)
        return None

    async def save(self, user: UserEntity) -> None:
        """ "
        Save user

        Parameters
        ----------
        user : UserEntity
            User entity

        Returns
        -------
        None
        """

        user_model = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
        )

        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
