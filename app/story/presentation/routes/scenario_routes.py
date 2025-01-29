from typing import List

from fastapi import APIRouter, Depends

from app.core.dependencies import get_scenario_use_case
from app.story.application.use_cases.get_scenarios import GetScenariosUseCase
from app.story.presentation.models.scenario import ScenarioResponse

router = APIRouter()


@router.get("/", response_model=List[ScenarioResponse])
async def get_scenarios(use_case: GetScenariosUseCase = Depends(get_scenario_use_case)):
    """Retrieve a list of available scenarios."""
    scenarios = await use_case.execute()

    return scenarios
