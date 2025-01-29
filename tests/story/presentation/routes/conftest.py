import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.story.domain.entities.scenario import Scenario as ScenarioEntity
from app.story.infrastructure.persistence.models.scenario import (
    Scenario as ScenarioModel,
)
from tests.utils.fakers import ScenarioFactory


@pytest.fixture(scope="function")
async def created_scenario(async_db_session: AsyncSession) -> ScenarioModel:
    factory: ScenarioEntity = ScenarioFactory.create()
    db_model = ScenarioModel(name=factory.name, description=factory.description)

    async_db_session.add(db_model)
    await async_db_session.commit()

    return db_model
