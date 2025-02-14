import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI, Request
from httpx import ASGITransport, AsyncClient
from jose import JWTError

from app.auth.application.decorators.auth_decorator import require_auth

# Create a separate test app
test_app = FastAPI()


# This is a route definition, not a test
@test_app.get("/test-auth")
@require_auth
async def protected_endpoint(request: Request):
    return {"message": "success", "user_email": request.state.user.email}


@pytest_asyncio.fixture
async def test_client(mock_auth_service):
    """Create a test client with the test app"""
    test_app.state.auth_service = mock_auth_service

    # Configure the client with proper ASGI transport
    async with LifespanManager(test_app):
        async with AsyncClient(
            transport=ASGITransport(app=test_app),
            base_url="http://test",
            follow_redirects=True,
        ) as client:
            yield client


@pytest.mark.asyncio
async def test_missing_token(test_client):
    """Test request without authentication token"""
    response = await test_client.get("/test-auth")

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_invalid_auth_scheme(test_client):
    """Test request with wrong authentication scheme"""
    headers = {"Authorization": "Basic some-token"}
    response = await test_client.get("/test-auth", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication scheme"
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_invalid_token_format(test_client, mock_auth_service):
    """Test request with malformed token"""
    # Configure mock to raise JWTError
    mock_auth_service.verify_token.side_effect = JWTError("Invalid token format")
    headers = {"Authorization": "Bearer invalid.token.format"}

    response = await test_client.get("/test-auth", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_missing_email_in_payload(test_client, mock_auth_service):
    """Test token with missing email in payload"""
    # Configure mock to return empty payload
    mock_auth_service.configure_verify_token({})
    headers = {"Authorization": "Bearer valid.token"}

    response = await test_client.get("/test-auth", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token payload"


@pytest.mark.asyncio
async def test_user_not_found(test_client, mock_auth_service):
    """Test when user from token not found in database"""
    # Configure mocks
    mock_auth_service.configure_verify_token({"email": "test@example.com"})
    mock_auth_service.configure_get_by_email(None)
    headers = {"Authorization": "Bearer valid.token"}

    response = await test_client.get("/test-auth", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_inactive_user(test_client, mock_auth_service, test_user):
    """Test when user is inactive"""
    # Configure test user and mocks
    test_user.is_active = False
    mock_auth_service.configure_verify_token({"email": test_user.email})
    mock_auth_service.configure_get_by_email(test_user)
    headers = {"Authorization": "Bearer valid.token"}

    response = await test_client.get("/test-auth", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Inactive user"


@pytest.mark.asyncio
async def test_successful_authentication(test_client, mock_auth_service, test_user):
    """Test successful authentication flow"""
    # Configure mocks for successful authentication
    mock_auth_service.configure_verify_token({"email": test_user.email})
    mock_auth_service.configure_get_by_email(test_user)
    headers = {"Authorization": "Bearer valid.token"}

    response = await test_client.get("/test-auth", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "success", "user_email": test_user.email}


@pytest.mark.asyncio
async def test_multiple_requests_same_user(test_client, mock_auth_service, test_user):
    """Test multiple authenticated requests with the same user"""
    # Configure mocks for successful authentication
    mock_auth_service.configure_verify_token({"email": test_user.email})
    mock_auth_service.configure_get_by_email(test_user)
    headers = {"Authorization": "Bearer valid.token"}

    for _ in range(3):
        response = await test_client.get("/test-auth", headers=headers)
        assert response.status_code == 200
        assert response.json()["user_email"] == test_user.email


@pytest.mark.asyncio
async def test_general_exception_handling(test_client, mock_auth_service):
    """Test handling of unexpected exceptions during authentication"""
    # Configure mock to raise an unexpected exception
    mock_auth_service.verify_token.side_effect = RuntimeError("Unexpected error")
    headers = {"Authorization": "Bearer valid.token"}

    response = await test_client.get("/test-auth", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
    assert response.headers["WWW-Authenticate"] == "Bearer"
