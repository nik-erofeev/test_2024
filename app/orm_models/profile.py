from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import orm_models
from app.orm_models import IdMixin
from app.utils.db import Base


class Profile(IdMixin, Base):
    first_name: Mapped[str | None] = mapped_column(String(30))
    last_name: Mapped[str | None] = mapped_column(String(30))
    bio: Mapped[str | None] = mapped_column(String(50))

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), unique=True)
    user: Mapped["orm_models.User"] = relationship(
        "User",
        back_populates='profile',
    )
