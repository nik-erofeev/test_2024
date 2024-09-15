from uuid import UUID

from sqlalchemy import select, update

from app.models.product import ProductCreate, ProductUpdate
from app.orm_models import Product
from app.utils.db import Db


class ProductRepo:
    def __init__(self, db: Db):
        self._db = db

    async def add_product(self, product: ProductCreate) -> Product:
        async with self._db.get_session() as session:
            product_dict = product.model_dump()

            product_model = Product(**product_dict)
            session.add(product_model)
            await session.flush()
            await session.commit()
            return product_model

    async def get_product_id(self, product_id: UUID) -> Product | None:
        async with self._db.get_session() as session:
            query = select(Product).filter_by(id=product_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_product_pagination(self, page: int, per_page: int) -> list[Product]:
        async with self._db.get_session() as session:
            query = select(Product).offset((page - 1) * per_page).limit(per_page)
            result = await session.execute(query)
            products = result.scalars()
            return list(products)

    async def update_product(self, product_id: UUID, product_update: ProductUpdate) -> bool:
        async with self._db.get_session() as session:

            update_data = product_update.model_dump(exclude_unset=True)
            if not update_data:
                return False

            await session.execute(update(Product).where(Product.id == product_id).values(**update_data))
            await session.commit()

            return True

    # async def delete_product(self, product_id: UUID):
    #     async with self._db.get_session() as session:
