import pytest
from httpx import AsyncClient

from app.auth.domain.entities.user import User


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    register_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "123123",
    }

    response = await async_client.post("/auth/register", json=register_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "John Doe"
    assert response_data["email"] == "john.doe@example.com"
    assert response_data["message"] == "User registered successfully."


@pytest.mark.asyncio
async def test_register_duplicated_email(
    async_client: AsyncClient, registered_user: User
):
    register_data = {
        "name": registered_user.name,
        "email": registered_user.email,
        "password": registered_user.hashed_password,
    }

    response = await async_client.post("/auth/register", json=register_data)

    assert response.status_code == 400
    response_data = response.json()
    assert (
        response_data["detail"]
        == f"User with email {registered_user.email} is already registered"
    )


@pytest.mark.asyncio
async def test_login_user_success(async_client: AsyncClient, registered_user: User):
    login_data = {
        "email": registered_user.email,
        "password": registered_user.hashed_password,
    }

    response = await async_client.post("/auth/login", json=login_data)

    assert response.status_code == 200

    response_data = response.json()

    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client: AsyncClient):
    login_data = {"email": "invalid_email@example.com", "password": "invalid_password"}

    response = await async_client.post("/auth/login", json=login_data)

    assert response.status_code == 400
