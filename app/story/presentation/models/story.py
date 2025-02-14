from typing import List

from pydantic import BaseModel, Field

from app.character.presentation.models.character import CharacterResponse
from app.scenario.presentation.models.scenario import ScenarioResponse


class GenerateStoryRequest(BaseModel):
    """Request model for generating a story."""

    character_ids: List[str] = Field(
        ..., examples=["123e4567-e89b-12d3-a456-426614174000"], min_length=1
    )
    scenario_id: str = Field(..., examples=["123e4567-e89b-12d3-a456-426614174001"])
    narrative_style: str = Field(
        ..., examples=["adventurous"], description="The storytelling style."
    )


class GenerateStoryResponse(BaseModel):
    """Response model for the generated story."""

    title: str = Field(..., examples=["The Adventures of Luna and the Magic Forest"])
    content: str = Field(..., examples=["Once upon a time in a magical forest..."])
    characters: List[CharacterResponse]
    scenario: ScenarioResponse
    narrative_style: str = Field(
        ..., examples=["adventurous"], description="The storytelling style."
    )
