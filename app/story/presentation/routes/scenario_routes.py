from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.dependencies import (
    create_scenario_use_case,
    get_scenario_use_case,
    get_scenarios_use_case,
)
from app.story.application.use_cases.create_scenario import CreateScenarioUseCase
from app.story.application.use_cases.get_scenario import GetScenarioUseCase
from app.story.application.use_cases.get_scenarios import GetScenariosUseCase
from app.story.domain.exceptions.scenario_exceptions import (
    InvalidScenarioDataError,
    ScenarioAlreadyExistsError,
)
from app.story.presentation.models.scenario import ScenarioRequest, ScenarioResponse

router = APIRouter()


@router.get("/", response_model=List[ScenarioResponse])
async def get_scenarios(
    use_case: GetScenariosUseCase = Depends(get_scenarios_use_case),
):
    """
    Fetches a list of scenarios using the provided use case.

    Returns
    -------
    list
        A list of scenarios fetched by the use case.
    """
    scenarios = await use_case.execute()

    return scenarios


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: UUID,
    use_case: GetScenarioUseCase = Depends(get_scenario_use_case),
):
    """
    Retrieve a scenario using the provided use case.

    Returns
    -------
    ScenarioResponse
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


@router.post("/", response_model=ScenarioResponse)
async def create_scenario(
    scenario: ScenarioRequest,
    use_case: CreateScenarioUseCase = Depends(create_scenario_use_case),
):
    """
    Create a scenario using the provided use case.

    Parameters
    ----------
    scenario: ScenarioRequest
        data to be create a scenario

    Returns
    -------
    ScenarioResponse
        Created scenario

    Raises
    ------
    HTTPException
        If the scenario cannot be created.
    """
    try:
        created_scenario = await use_case.execute(
            name=scenario.name, description=scenario.description
        )

        return created_scenario
    except (InvalidScenarioDataError, ScenarioAlreadyExistsError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
