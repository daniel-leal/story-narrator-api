from abc import ABC, abstractmethod
from typing import List

from app.story.domain.entities.scenario import Scenario as ScenarioEntity


class BaseScenarioRepository(ABC):
    """Abstract base class for the scenario repository."""

    @abstractmethod
    async def get_all(self) -> List[ScenarioEntity]:
        """Retrieve all available scenarios."""
