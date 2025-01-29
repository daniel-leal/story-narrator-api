from uuid import UUID

from pydantic import BaseModel, Field


class ScenarioResponse(BaseModel):
    id: UUID
    name: str = Field(
        ...,
        examples=[
            "Enchanted Forest",
            "Space Adventure",
            "Ice Kindgom",
        ],
        description="Name of scenario",
    )
    description: str = Field(
        ...,
        examples=[
            "A magical forest where trees whisper secrets...",
            "Deep in space, among twinkling stars and colorful planets...",
            " A frozen wonderland where snow never melts...",
        ],
        description="A description of visual objects and itens of the scenario",
    )
