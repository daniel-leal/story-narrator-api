from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.scenario.domain.entities.scenario import Scenario as ScenarioEntity


class BaseScenarioRepository(ABC):
    """Abstract base class for the scenario repository."""

    @abstractmethod
    async def get_all(self) -> List[ScenarioEntity]:
        """
        Retrieve all available scenarios.

        Returns
        -------
        List[ScenarioEntity]
            A list of all available ScenarioEntity objects.
        """

    @abstractmethod
    async def get_by_id(self, scenario_id: UUID) -> ScenarioEntity | None:
        """
        Retrieve a scenario by its ID.

        Parameters
        ----------
        scenario_id : UUID
            The unique identifier of the scenario to retrieve.

        Returns
        -------
        ScenarioEntity or None
            The scenario entity if found, otherwise None.
        """

    @abstractmethod
    async def get_by_name(self, name: str) -> ScenarioEntity | None:
        """
        Retrieve a scenario by its Name.

        Parameters
        ----------
        name : str
            The name of the scenario to retrieve.

        Returns
        -------
        ScenarioEntity or None
            The scenario entity if found, otherwise None.
        """

    @abstractmethod
    async def save(self, scenario: ScenarioEntity) -> ScenarioEntity:
        """
        Save a scenario entity to the repository.

        Parameters
        ----------
        scenario : ScenarioEntity
            The scenario entity to be saved.

        Returns
        -------
        ScenarioEntity
            The saved scenario entity.
        """
