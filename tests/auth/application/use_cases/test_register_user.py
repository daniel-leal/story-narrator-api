import pytest

from app.auth.application.use_cases.register_user import RegisterUserUseCase
from app.auth.domain.entities.user import User
from app.auth.domain.exceptions.user_exceptions import UserAlreadyRegisteredError
from tests.utils.mocks import MockAuthService


@pytest.fixture
def mock_auth_service():
    return MockAuthService()


@pytest.fixture
def register_user_use_case(mock_auth_service):
    return RegisterUserUseCase(auth_service=mock_auth_service)


@pytest.mark.asyncio
async def test_register_user_success(register_user_use_case, mock_auth_service):
    user = User(
        name="John Doe",
        email="john.doe@example.com",
        hashed_password="hashed_password",
    )
    mock_auth_service.configure_register_user(user)

    result = await register_user_use_case.execute(
        name="John Doe", email="john.doe@example.com", password="password"
    )

    assert result.name == "John Doe"
    assert result.email == "john.doe@example.com"
    mock_auth_service.register_user.assert_awaited_once_with(
        "John Doe", "john.doe@example.com", "password"
    )


@pytest.mark.asyncio
async def test_register_user_service_failure(register_user_use_case, mock_auth_service):
    mock_auth_service.register_user.side_effect = UserAlreadyRegisteredError(
        "john.doe@example.com"
    )

    with pytest.raises(UserAlreadyRegisteredError) as exc_info:
        await register_user_use_case.execute(
            name="John Doe", email="john.doe@example.com", password="password"
        )

    assert (
        str(exc_info.value)
        == "User with email john.doe@example.com is already registered"
    )
    mock_auth_service.register_user.assert_awaited_once_with(
        "John Doe", "john.doe@example.com", "password"
    )
