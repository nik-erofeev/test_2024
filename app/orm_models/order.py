from datetime import datetime

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import orm_models
from app.orm_models import IdMixin
from app.utils.db import Base


class Order(IdMixin, Base):

    __tablename__ = 'orders'

    promocode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )

    products: Mapped[list["orm_models.Product"]] = relationship(
        "Product",
        secondary="orders_products",
        back_populates='orders',
    )
