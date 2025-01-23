from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """Base model for all models in the application."""

    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
