from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import BaseModel as Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"
