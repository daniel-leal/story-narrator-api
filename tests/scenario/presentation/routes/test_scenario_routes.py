from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.scenario.domain.entities.scenario import Scenario


@pytest.mark.asyncio
async def test_get_all_scenarios(async_client: AsyncClient, created_scenario: Scenario):
    response = await async_client.get("/scenarios/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["name"] == created_scenario.name
    assert data[0]["description"] == created_scenario.description


@pytest.mark.asyncio
async def test_get_scenario_by_id(
    async_client: AsyncClient, created_scenario: Scenario
):
    response = await async_client.get(f"/scenarios/{created_scenario.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == created_scenario.name
    assert data["description"] == created_scenario.description


@pytest.mark.asyncio
async def test_get_scenario_by_id_not_found(async_client: AsyncClient):
    non_existent_id = uuid4()
    response = await async_client.get(f"/scenarios/{non_existent_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Scenario not found"


@pytest.mark.asyncio
async def test_create_scenario(async_client: AsyncClient):
    scenario_data = {"name": "New Scenario", "description": "New Description"}
    response = await async_client.post("/scenarios/", json=scenario_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == scenario_data["name"]
    assert data["description"] == scenario_data["description"]


@pytest.mark.asyncio
async def test_create_scenario_invalid_data(async_client: AsyncClient):
    scenario_data = {"name": "", "description": ""}

    response = await async_client.post("/scenarios/", json=scenario_data)

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
