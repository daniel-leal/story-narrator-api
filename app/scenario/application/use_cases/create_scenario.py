from app.scenario.domain.entities.scenario import Scenario
from app.scenario.domain.exceptions.scenario_exceptions import (
    InvalidScenarioDataError,
    ScenarioAlreadyExistsError,
)
from app.scenario.domain.interfaces.scenario_repository import BaseScenarioRepository


class CreateScenarioUseCase:
    def __init__(self, scenario_repository: BaseScenarioRepository) -> None:
        self.scenario_repository = scenario_repository

    async def execute(self, name: str, description: str) -> Scenario:
        """
        Execute the use case to create a new scenario.

        Parameters
        ----------
        scenario_data : dict
            A dictionary containing the data required to create a new scenario.

        Returns
        -------
        scenario : Scenario
            The newly created scenario object.

        Raises
        ------
        ValidationError
            If the scenario data is invalid.
        RepositoryError
            If there is an error saving the scenario to the repository.
        """

        self._validate_scenario_data(name, description)

        existing_scenario = await self.scenario_repository.get_by_name(name)
        if existing_scenario:
            raise ScenarioAlreadyExistsError(f"Scenario '{name}' already exists.")

        scenario = Scenario(name=name, description=description)

        return await self.scenario_repository.save(scenario)

    def _validate_scenario_data(self, name: str, description: str) -> None:
        """
        Validates the scenario data before saving.

        Raises
        ------
        InvalidScenarioDataError
            If the provided data does not meet validation rules.
        """

        if not name or not description:
            raise InvalidScenarioDataError("Name and description cannot be empty.")

        if len(name) > 100:
            raise InvalidScenarioDataError(
                "Scenario name cannot exceed 100 characters."
            )

        if len(description) > 500:
            raise InvalidScenarioDataError(
                "Scenario description cannot exceed 500 characters."
            )
