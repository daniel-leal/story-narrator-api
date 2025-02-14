from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Scenario(BaseModel):
    """Domain entity representing a story scenario."""

    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    available: bool = True

    model_config = ConfigDict(from_attributes=True)
