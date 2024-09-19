from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import orm_models
from app.orm_models import IdMixin
from app.utils.db import Base


class User(IdMixin, Base):
    username: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    posts: Mapped[list["orm_models.Post"]] = relationship(
        "Post",
        back_populates='user',
    )  # todo: O-t-M (у юзера - постЫ)

    profile: Mapped["orm_models.Profile"] = relationship(
        "Profile",
        back_populates='user',
    )  # todo O-t-O
