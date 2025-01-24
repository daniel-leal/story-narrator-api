from uuid import UUID

from pydantic import BaseModel, Field


class CreateCharacterRequest(BaseModel):
    """
    Request model for creating a new character.
    """

    name: str = Field(
        ...,
        examples=["Luna", "Max", "Ruby"],
        description="The name of the character.",
    )
    favorite_color: str = Field(
        ...,
        examples=["Blue", "Green", "Red"],
        description="The favorite color of the character.",
    )
    animal_friend: str = Field(
        ...,
        examples=["Fox", "Rabbit", "Bear"],
        description="The character's animal friend.",
    )
    superpower: str = Field(
        ...,
        examples=["Invisibility", "Flying", "Strength"],
        description="The character's superpower.",
    )
    hobby: str = Field(
        ...,
        examples=["Painting", "Dancing", "Singing"],
        description="The character's hobby.",
    )
    personality: str = Field(
        ...,
        examples=["Adventurous", "Shy", "Brave"],
        description="The personality traits of the character.",
    )


class CreateCharacterResponse(BaseModel):
    """
    Response model for the created character.
    """

    id: UUID
    name: str
    favorite_color: str
    animal_friend: str
    superpower: str
    hobby: str
    personality: str
