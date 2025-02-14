from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status

from app.auth.application.decorators.auth_decorator import require_auth
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
    responses={
        201: {"description": "Story generated successfully"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Inactive user"},
        422: {"description": "Validation Error - Invalid story parameters"},
    },
    openapi_extra={"security": [{"bearerAuth": []}]},
)
@require_auth
async def generate_story(
    request: Request,
    story_request: GenerateStoryRequest,
    story_use_case: GenerateStoryUseCase = Depends(get_generate_story_use_case),
):
    """
    Generate a story using the selected characters, scenario, and narrative style.

    Parameters
    ----------
    request : Request
        The FastAPI request object containing user state
    story_request : GenerateStoryRequest
        The request body containing character IDs, scenario ID, and narrative style
    story_use_case : GenerateStoryUseCase
        The use case for story generation, injected via dependency

    Returns
    -------
    GenerateStoryResponse
        The generated story response object

    Raises
    ------
    HTTPException
        If story validation fails with 422 status code
    """
    try:
        return await story_use_case.execute(
            character_ids=[UUID(cid) for cid in story_request.character_ids],
            scenario_id=UUID(story_request.scenario_id),
            narrative_style=story_request.narrative_style,
        )
    except StoryValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
