import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_scenario_repository
from app.scenario.domain.entities.scenario import Scenario as ScenarioEntity
from tests.utils.fakers import ScenarioFactory


@pytest.fixture(scope="function")
async def created_scenario(async_db_session: AsyncSession) -> ScenarioEntity:
    factory: ScenarioEntity = ScenarioFactory.create()

    scenario_repository = get_scenario_repository(async_db_session)

    return await scenario_repository.save(factory)
