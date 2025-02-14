from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.character.domain.entities.character import Character
from app.scenario.domain.entities.scenario import Scenario


class Story(BaseModel):
    """Entity representing a generated story."""

    id: Optional[UUID] = Field(default_factory=uuid4)
    title: str = Field(..., examples=["The Adventures of Luna and the Magic Forest"])
    content: str = Field(..., examples=["Once upon a time in a magical forest..."])
    characters: List[Character]
    scenario: Scenario
    narrative_style: str = Field(
        ..., examples=["adventurous", "action", "comedy", "fantasy"]
    )
