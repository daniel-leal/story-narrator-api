from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_character(async_client: AsyncClient):
    request_payload = {
        "name": "Test Character",
        "favorite_color": "Blue",
        "animal_friend": "Dog",
        "superpower": "Invisibility",
        "hobby": "Reading",
        "personality": "Brave",
    }

    response = await async_client.post("/characters/", json=request_payload)

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["name"] == request_payload["name"]
    assert response_data["favorite_color"] == request_payload["favorite_color"]
    assert response_data["animal_friend"] == request_payload["animal_friend"]
    assert response_data["superpower"] == request_payload["superpower"]
    assert response_data["hobby"] == request_payload["hobby"]
    assert response_data["personality"] == request_payload["personality"]


@pytest.mark.asyncio
async def test_create_character_invalid_data(async_client: AsyncClient):
    request_payload = {
        "name": "",
        "favorite_color": "Blue",
        "animal_friend": "Dog",
        "superpower": "Invisibility",
        "hobby": "Reading",
        "personality": "Brave",
    }

    response = await async_client.post("/characters/", json=request_payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_character_by_id(async_client: AsyncClient):
    character_id = uuid4()

    response = await async_client.get(f"/characters/{character_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Character with ID {character_id} not found."


@pytest.mark.asyncio
async def test_get_character_by_id_existing(
    async_client: AsyncClient, created_character
):
    character_id = created_character.id

    response = await async_client.get(f"/characters/{character_id}")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["name"] == created_character.name
    assert response_data["favorite_color"] == created_character.favorite_color
    assert response_data["animal_friend"] == created_character.animal_friend
    assert response_data["superpower"] == created_character.superpower
    assert response_data["hobby"] == created_character.hobby
    assert response_data["personality"] == created_character.personality
