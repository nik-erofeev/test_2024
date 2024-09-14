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

    async def get_product_by_name(self, name: str) -> Product:
        async with self._db.get_session() as session:
            # query = select(ProductsOrm).filter_by(name=name)
            # todo: учитываем регистр и нижний и верхний
            query = select(Product).filter(Product.name.ilike(f'%{name}%'))
            result = await session.execute(query)
            return result.scalar()

    async def get_product_pagination(self, page: int, per_page: int) -> list[Product]:
        async with self._db.get_session() as session:
            query = select(Product).offset((page - 1) * per_page).limit(per_page)
            result = await session.execute(query)
            products = result.scalars()
            return list(products)

    async def update_product(self, product_id: UUID, product_update: ProductUpdate) -> bool | None:
        async with self._db.get_session() as session:
            query = select(Product).filter_by(id=product_id)
            # query = select(Product).filter(Product.id == product_id)
            result = await session.execute(query)
            product = result.scalar_one_or_none()

            if not product:
                return None

            update_data = product_update.model_dump(exclude_unset=True)
            if not update_data:
                return False

            if update_data:
                await session.execute(update(Product).where(Product.id == product_id).values(**update_data))
                await session.commit()

            return True
