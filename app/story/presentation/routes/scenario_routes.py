from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_scenario_use_case, get_scenarios_use_case
from app.story.application.use_cases.get_scenario import GetScenarioUseCase
from app.story.application.use_cases.get_scenarios import GetScenariosUseCase
from app.story.presentation.models.scenario import ScenarioResponse

router = APIRouter()


@router.get("/", response_model=List[ScenarioResponse])
async def get_scenarios(
    use_case: GetScenariosUseCase = Depends(get_scenarios_use_case),
):
    """
    Fetches a list of scenarios using the provided use case.

    Parameters
    ----------
    use_case : GetScenariosUseCase, optional
        The use case to fetch scenarios, by default obtained from dependency injection.

    Returns
    -------
    list
        A list of scenarios fetched by the use case.
    """
    scenarios = await use_case.execute()

    return scenarios


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: UUID, use_case: GetScenarioUseCase = Depends(get_scenario_use_case)
):
    """
    Retrieve a scenario using the provided use case.

    Parameters
    ----------
    use_case : GetScenarioUseCase, optional
        The use case to retrieve the scenario, by default obtained from dependency injection.

    Returns
    -------
    Scenario
        The retrieved scenario object.

    Raises
    ------
    HTTPException
        If the scenario cannot be retrieved.
    """
    scenario = await use_case.execute(scenario_id=scenario_id)

    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return scenario
