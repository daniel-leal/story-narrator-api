from fastapi import APIRouter, Depends, HTTPException

from app.auth.application.use_cases.login_user import LoginUserUseCase
from app.auth.application.use_cases.register_user import RegisterUserUseCase
from app.auth.domain.services.auth_service import AuthService
from app.auth.presentation.models.auth import (
    LoginRequest,
    LoginResponse,
    RegisterUserRequest,
    RegisterUserResponse,
)
from app.core.dependencies import get_auth_service

router = APIRouter()


@router.post("/register", response_model=RegisterUserResponse)
async def register_user(
    request: RegisterUserRequest, auth_service: AuthService = Depends(get_auth_service)
):
    """
    API endpoint to register a new user.

    Parameters
    ----------
    request : RegisterUserRequest
        body containing the user data.
    """
    try:
        use_case = RegisterUserUseCase(auth_service)
        user = await use_case.execute(request.name, request.email, request.password)
        return RegisterUserResponse(
            name=user.name,
            email=user.email,
            message="User registered successfully.",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login_user(
    request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
):
    """
    API endpoint to login a user.

    Parameters
    ----------
    request : LoginRequest
        body containing the user email and password.
    """
    try:
        use_case = LoginUserUseCase(auth_service)
        token = await use_case.execute(request.email, request.password)
        return LoginResponse(access_token=token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
