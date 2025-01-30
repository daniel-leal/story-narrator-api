from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.story.domain.entities.scenario import Scenario as ScenarioEntity


class BaseScenarioRepository(ABC):
    """Abstract base class for the scenario repository."""

    @abstractmethod
    async def get_all(self) -> List[ScenarioEntity]:
        """Retrieve all available scenarios."""

    @abstractmethod
    async def get_by_id(self, scenario_id: UUID) -> ScenarioEntity | None:
        """Retrieve a scenario by its ID."""
