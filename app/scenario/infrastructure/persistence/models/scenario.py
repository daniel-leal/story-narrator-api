from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.infrastructure.persistence.models.base import BaseModel


class Scenario(BaseModel):
    """Model representing a story scenario."""

    __tablename__ = "scenarios"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
