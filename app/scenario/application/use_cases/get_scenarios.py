from typing import List

from app.scenario.domain.entities.scenario import Scenario
from app.scenario.domain.interfaces.scenario_repository import BaseScenarioRepository


class GetScenariosUseCase:
    """Use case to retrieve available scenarios."""

    def __init__(self, scenario_repository: BaseScenarioRepository) -> None:
        self.scenario_repository = scenario_repository

    async def execute(self) -> List[Scenario]:
        """
        Returns a list of available scenarios.

        Returns
        -------
        List of Scenario
            The list of scenarios of a story
        """
        return await self.scenario_repository.get_all()
