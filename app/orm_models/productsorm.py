from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.orm_models import IdMixin
from app.utils.db import Base


class ProductsOrm(IdMixin, Base):

    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
