from uuid import UUID

from app.story.domain.entities.scenario import Scenario
from app.story.domain.interfaces.scenario_repository import BaseScenarioRepository


class GetScenarioUseCase:
    """Use case to retrieve available scenarios."""

    def __init__(self, scenario_repository: BaseScenarioRepository) -> None:
        self.scenario_repository = scenario_repository

    async def execute(self, scenario_id: UUID) -> Scenario | None:
        """
        Retrieve a scenario by its ID.

        Parameters
        ----------
        scenario_id : UUID
            The unique identifier of the scenario to retrieve.

        Returns
        -------
        Scenario or None
            The scenario object if found, otherwise None.
        """

        return await self.scenario_repository.get_by_id(scenario_id)
