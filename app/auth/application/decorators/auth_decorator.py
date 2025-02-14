from functools import wraps
from typing import Callable

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jose import JWTError

security = HTTPBearer()


def require_auth(func: Callable) -> Callable:
    """
    Decorator for routes that require authentication.
    Verifies the JWT token and ensures the user is authenticated.

    Returns
    -------
    callable
        Decorated function.

    Raises
    ------
    HTTPException
        401 if token is invalid or missing
        403 if user is inactive
    """

    @wraps(func)
    async def wrapper(
        *args,
        request: Request,
        **kwargs,
    ):
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                raise HTTPException(
                    status_code=401,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication scheme",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            auth_service = request.app.state.auth_service

            try:
                payload = auth_service.verify_token(token)
                email = payload.get("email")

                if not email:
                    raise HTTPException(
                        status_code=401,
                        detail="Invalid token payload",
                    )

                user = await auth_service.user_repository.get_by_email(email)
                if not user:
                    raise HTTPException(
                        status_code=401,
                        detail="User not found",
                    )

                if not user.is_active:
                    raise HTTPException(
                        status_code=403,
                        detail="Inactive user",
                    )

                request.state.user = user
                return await func(*args, request=request, **kwargs)

            except JWTError:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return wrapper
