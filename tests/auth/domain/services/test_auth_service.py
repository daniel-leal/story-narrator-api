from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.auth.domain.entities.user import User
from app.auth.domain.exceptions.user_exceptions import UserAlreadyRegisteredError
from app.auth.domain.services.auth_service import AuthService
from tests.utils.mocks import MockUserRepository


@pytest.fixture
def mock_user_repository():
    return MockUserRepository()


@pytest.fixture
def auth_service(mock_user_repository):
    service = AuthService(mock_user_repository)

    return service


@pytest.fixture
def valid_payload():
    """Create a valid token payload"""
    return {
        "sub": "123e4567-e89b-12d3-a456-426614174000",
        "email": "test@example.com",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }


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


def test_create_access_token(auth_service, test_settings):
    user = User(
        name="John Doe",
        email="john.doe@example.com",
        hashed_password="hashed_pwd",
        is_active=True,
    )

    token = auth_service.create_access_token(user)

    from datetime import datetime, timezone

    import jwt

    secret_key = test_settings.JWT_SECRET_KEY
    algorithm = test_settings.JWT_ALGORITHM
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])

    assert payload["sub"] == str(user.id)
    assert payload["email"] == user.email
    assert "exp" in payload

    exp_timestamp = payload["exp"]
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    assert exp_datetime > datetime.now(timezone.utc)


def test_verify_valid_token(auth_service, valid_payload, test_settings):
    """Test verification of a valid token succeeds"""
    # Arrange
    secret_key = test_settings.JWT_SECRET_KEY
    algorithm = test_settings.JWT_ALGORITHM
    token = jwt.encode(valid_payload, secret_key, algorithm=algorithm)

    # Act
    decoded_payload = auth_service.verify_token(token)

    # Assert
    assert decoded_payload["email"] == valid_payload["email"]
    assert decoded_payload["sub"] == valid_payload["sub"]


def test_verify_expired_token(auth_service):
    """Test verification of an expired token fails"""
    # Arrange
    secret_key = "nKDXqKoG/pgP2rK7vsz2nHVbzl/2z/vWLGWzgiYcpVZaAQo941tg7Oeg"
    algorithm = "HS256"
    expired_payload = {
        "sub": "123e4567-e89b-12d3-a456-426614174000",
        "email": "test@example.com",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=30),
    }
    token = jwt.encode(expired_payload, secret_key, algorithm=algorithm)

    # Act & Assert
    with pytest.raises(jwt.ExpiredSignatureError):
        auth_service.verify_token(token)


def test_verify_invalid_signature(auth_service, valid_payload):
    """Test verification of token with invalid signature fails"""
    # Arrange
    wrong_secret = "wrong_secret_key"
    algorithm = "HS256"
    token = jwt.encode(valid_payload, wrong_secret, algorithm=algorithm)

    # Act & Assert
    with pytest.raises(jwt.InvalidSignatureError):
        auth_service.verify_token(token)


def test_verify_invalid_token_format(auth_service):
    """Test verification of malformed token fails"""
    # Arrange
    invalid_token = "invalid.token.format"

    # Act & Assert
    with pytest.raises(jwt.InvalidTokenError):
        auth_service.verify_token(invalid_token)


def test_verify_token_missing_claims(auth_service):
    """Test verification of token with missing claims"""
    # Arrange
    secret_key = "nKDXqKoG/pgP2rK7vsz2nHVbzl/2z/vWLGWzgiYcpVZaAQo941tg7Oeg"
    algorithm = "HS256"
    incomplete_payload = {
        "sub": "123e4567-e89b-12d3-a456-426614174000",
        # missing email and exp
    }
    token = jwt.encode(incomplete_payload, secret_key, algorithm=algorithm)

    # Act
    decoded_payload = auth_service.verify_token(token)

    # Assert
    assert "email" not in decoded_payload
    assert decoded_payload["sub"] == incomplete_payload["sub"]


def test_verify_token_with_different_algorithm(auth_service, valid_payload):
    """Test verification of token with wrong algorithm fails"""
    # Arrange
    secret_key = "nKDXqKoG/pgP2rK7vsz2nHVbzl/2z/vWLGWzgiYcpVZaAQo941tg7Oeg"
    token = jwt.encode(valid_payload, secret_key, algorithm="HS512")

    # Act & Assert
    with pytest.raises(jwt.InvalidAlgorithmError):
        auth_service.verify_token(token)


def test_token_verification_end_to_end(auth_service):
    """Test complete flow of token creation and verification"""
    # Arrange
    user = User(
        name="John Doe",
        email="john.doe@example.com",
        hashed_password="hashed_pwd",
        is_active=True,
    )

    # Act
    token = auth_service.create_access_token(user)
    decoded_payload = auth_service.verify_token(token)

    # Assert
    assert decoded_payload["email"] == user.email
    assert decoded_payload["sub"] == str(user.id)
    assert "exp" in decoded_payload
