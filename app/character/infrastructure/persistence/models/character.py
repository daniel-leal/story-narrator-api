from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.persistence.models.base import BaseModel


class Character(BaseModel):
    """Character model"""

    __tablename__ = "characters"

    name: Mapped[str] = mapped_column(String, nullable=False)
    favorite_color: Mapped[str] = mapped_column(String, nullable=True)
    animal_friend: Mapped[str] = mapped_column(String, nullable=True)
    superpower: Mapped[str] = mapped_column(String, nullable=True)
    hobby: Mapped[str] = mapped_column(String, nullable=True)
    personality: Mapped[str] = mapped_column(String, nullable=True)
    personality: Mapped[str] = mapped_column(String, nullable=True)
