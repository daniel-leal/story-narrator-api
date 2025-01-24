from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    """User entity"""

    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
