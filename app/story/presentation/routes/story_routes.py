from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.dependencies import get_generate_story_use_case
from app.story.application.use_cases.generate_story import GenerateStoryUseCase
from app.story.domain.exceptions.story_exceptions import StoryValidationError
from app.story.presentation.models.story import (
    GenerateStoryRequest,
    GenerateStoryResponse,
)

router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerateStoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_story(
    request: GenerateStoryRequest,
    story_use_case: GenerateStoryUseCase = Depends(get_generate_story_use_case),
):
    """
    Generate a story using the selected characters, scenario, and narrative style.

    Parameters
    ----------
    request: GenerateStoryRequest
        The request body containing character IDs, scenario ID, and narrative style.

    Returns
    -------
    GenerateStoryResponse
        The generated story.
    """
    try:
        return await story_use_case.execute(
            character_ids=[UUID(cid) for cid in request.character_ids],
            scenario_id=UUID(request.scenario_id),
            narrative_style=request.narrative_style,
        )
    except StoryValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
