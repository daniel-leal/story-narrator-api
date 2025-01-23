import pytest

from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import UserAlreadyRegisteredError
from app.domain.services.auth_service import AuthService
from tests.utils.mocks import MockUserRepository


@pytest.fixture
def mock_user_repository():
    """Fixture for a mocked UserRepository"""
    return MockUserRepository()


@pytest.fixture
def auth_service(mock_user_repository):
    return AuthService(mock_user_repository)


def test_hash_password(auth_service):
    password = "securepassword"
    hashed_password = auth_service.hash_password(password)

    assert hashed_password != password
    assert auth_service.pwd_context.verify(password, hashed_password)


def test_verify_password(auth_service):
    password = "securepassword"
    hashed_password = auth_service.hash_password(password)

    assert auth_service.verify_password(password, hashed_password)
    assert not auth_service.verify_password("wrongpassword", hashed_password)


@pytest.mark.asyncio
async def test_register_user_success(auth_service, mock_user_repository):
    mock_user_repository.get_by_email.return_value = None

    user = await auth_service.register_user(
        name="John Doe", email="john.doe@example.com", password="password"
    )

    assert user.name == "John Doe"
    assert user.email == "john.doe@example.com"

    mock_user_repository.get_by_email.assert_called_once_with("john.doe@example.com")
    mock_user_repository.save.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_register_user_email_exists(auth_service, mock_user_repository):
    existing_user = User(
        name="Existing User",
        email="existing@example.com",
        hashed_password="hashed_pwd",
    )
    mock_user_repository.configure_get_by_email(existing_user)

    with pytest.raises(UserAlreadyRegisteredError) as exc_info:
        await auth_service.register_user(
            name="John Doe", email="existing@example.com", password="password"
        )

    assert (
        str(exc_info.value)
        == "User with email existing@example.com is already registered"
    )

    mock_user_repository.get_by_email.assert_called_once_with("existing@example.com")
    mock_user_repository.save.assert_not_called()


def test_create_access_token(auth_service):
    user = User(
        name="John Doe",
        email="john.doe@example.com",
        hashed_password="hashed_pwd",
        is_active=True,
    )

    token = auth_service.create_access_token(user)

    from datetime import datetime, timezone

    import jwt

    secret_key = "nKDXqKoG/pgP2rK7vsz2nHVbzl/2z/vWLGWzgiYcpVZaAQo941tg7Oeg"
    algorithm = "HS256"
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])

    assert payload["sub"] == str(user.id)
    assert payload["email"] == user.email
    assert "exp" in payload

    exp_timestamp = payload["exp"]
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    assert exp_datetime > datetime.now(timezone.utc)
