import pytest
from fastapi import HTTPException

from app.application.use_cases.login_user import LoginUserUseCase
from app.domain.entities.user import User
from tests.utils.mocks import MockAuthService


@pytest.fixture
def mock_auth_service():
    """Fixture for a mocked AuthService."""
    return MockAuthService()


@pytest.fixture
def login_user_use_case(mock_auth_service):
    """Fixture for LoginUserUseCase."""
    return LoginUserUseCase(auth_service=mock_auth_service)


@pytest.mark.asyncio
async def test_login_user_success(login_user_use_case, mock_auth_service):
    user = User(
        name="John Doe",
        email="john.doe@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )
    mock_auth_service.configure_get_by_email(user)
    mock_auth_service.verify_password.return_value = True
    mock_auth_service.create_access_token.return_value = "fake_token"

    token = await login_user_use_case.execute(
        email="john.doe@example.com", password="password"
    )

    assert token == "fake_token"
    mock_auth_service.user_repository.get_by_email.assert_awaited_once_with(
        "john.doe@example.com"
    )
    mock_auth_service.verify_password.assert_called_once_with(
        "password", "hashed_password"
    )
    mock_auth_service.create_access_token.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_login_user_service_failure_invalid_credentials(
    login_user_use_case, mock_auth_service
):
    mock_auth_service.user_repository.get_by_email.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await login_user_use_case.execute(
            email="john.doe@example.com", password="wrong_password"
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password"


@pytest.mark.asyncio
async def test_login_user_invalid_password(login_user_use_case, mock_auth_service):
    user = User(
        name="John Doe",
        email="john.doe@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )
    mock_auth_service.configure_get_by_email(user)
    mock_auth_service.verify_password.return_value = False

    with pytest.raises(HTTPException) as exc_info:
        await login_user_use_case.execute(
            email="john.doe@example.com", password="wrong_password"
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password"


@pytest.mark.asyncio
async def test_login_user_service_failure_inactive_user(
    login_user_use_case, mock_auth_service
):
    user = User(
        name="John Doe",
        email="john.doe@example.com",
        hashed_password="hashed_password",
        is_active=False,
    )
    mock_auth_service.user_repository.get_by_email.return_value = user
    mock_auth_service.verify_password.return_value = True

    with pytest.raises(HTTPException) as exc_info:
        await login_user_use_case.execute(
            email="john.doe@example.com", password="password"
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Inactive user"
