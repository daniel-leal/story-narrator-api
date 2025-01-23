from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.domain.services.auth_service import AuthService
from app.infrastructure.repositories.user_repository import UserRepository


async def get_auth_service(
    db: AsyncSession = Depends(get_async_session),
) -> AuthService:
    """
    Dependency that initializes AuthService with a UserRepository instance.

    Parameters
    ----------
    db : Session
        SQLAlchemy session instance.

    Returns
    -------
    AuthService
        AuthService instance.
    """
    user_repository = UserRepository(db)
    return AuthService(user_repository)
