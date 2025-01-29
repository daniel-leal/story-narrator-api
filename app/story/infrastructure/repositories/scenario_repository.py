from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.story.domain.entities.scenario import Scenario as ScenarioEntity
from app.story.domain.interfaces.scenario_repository import BaseScenarioRepository
from app.story.infrastructure.persistence.models.scenario import (
    Scenario as ScenarioModel,
)


class ScenarioRepository(BaseScenarioRepository):
    """Implementation of scenario repository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> List[ScenarioEntity]:
        """
        Retrieve all available scenarios.

        Returns
        -------
        List[ScenarioEntity]
            A list of Scenario objects representing all available scenarios.
        """
        result = await self.session.execute(
            select(ScenarioModel).filter_by(available=True)
        )

        scenarios = result.scalars().all()

        return [ScenarioEntity.model_validate(scenario) for scenario in scenarios]
