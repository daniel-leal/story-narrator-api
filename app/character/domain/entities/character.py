from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Character(BaseModel):
    """Domain entity for a character."""

    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str = Field(min_length=1)
    favorite_color: Optional[str] = None
    animal_friend: Optional[str] = None
    superpower: Optional[str] = None
    hobby: Optional[str] = None
    personality: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
