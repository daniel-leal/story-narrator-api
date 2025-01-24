from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.character.application.use_cases.create_character import CreateCharacterUseCase
from app.character.domain.entities.character import Character
from app.character.infrastructure.repositories.character_repository import (
    CharacterRepository,
)
from app.character.presentation.models.character import (
    CreateCharacterRequest,
    CreateCharacterResponse,
)
from app.core.dependencies import (
    get_character_repository,
    get_create_character_use_case,
)

router = APIRouter()


@router.post(
    "/", response_model=CreateCharacterResponse, status_code=status.HTTP_201_CREATED
)
async def create_character(
    request: CreateCharacterRequest,
    create_character_use_case: CreateCharacterUseCase = Depends(
        get_create_character_use_case
    ),
):
    """
    Endpoint to create a new character.

    Parameters
    ----------
    request : CreateCharacterRequest
        The request body containing character details.
    create_character_use_case : CreateCharacterUseCase
        The use case for creating characters.

    Returns
    -------
    CreateCharacterResponse
        The created character response.
    """
    try:
        character = await create_character_use_case.execute(
            name=request.name,
            favorite_color=request.favorite_color,
            animal_friend=request.animal_friend,
            superpower=request.superpower,
            hobby=request.hobby,
            personality=request.personality,
        )
        return CreateCharacterResponse(**character.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{character_id}", response_model=Character, status_code=status.HTTP_200_OK)
async def get_character_by_id(
    character_id: UUID,
    character_repository: CharacterRepository = Depends(get_character_repository),
):
    """
    API endpoint to retrieve a character by its ID.

    Parameters
    ----------
    character_id : UUID
        The unique identifier of the character.

    Returns
    -------
    Character
        The character entity if found.
    """
    character = await character_repository.get_by_id(character_id)

    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with ID {character_id} not found.",
        )

    return character
