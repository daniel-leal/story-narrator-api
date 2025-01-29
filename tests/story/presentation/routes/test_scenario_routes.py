import pytest
from httpx import AsyncClient

from app.story.infrastructure.persistence.models.scenario import Scenario


@pytest.mark.asyncio
async def test_get_all_scenarios(async_client: AsyncClient, created_scenario: Scenario):
    response = await async_client.get("/scenarios/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["name"] == created_scenario.name
    assert data[0]["description"] == created_scenario.description
