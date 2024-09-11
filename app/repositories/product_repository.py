from sqlalchemy import select

from app.models.product import ProductCreate
from app.orm_models import ProductsOrm
from app.utils.db import Db


class ProductRepo:
    def __init__(self, db: Db):
        self._db = db

    async def add_product(self, product_dict: ProductCreate) -> ProductsOrm:
        async with self._db.get_session() as session:
            product_dict = product_dict.model_dump()

            product = ProductsOrm(**product_dict)
            session.add(product)
            await session.flush()
            await session.commit()
            return product

    async def get_product_by_name(self, name: str) -> ProductsOrm:
        async with self._db.get_session() as session:
            # query = select(ProductsOrm).filter_by(name=name)
            # todo: учитываем регистр и нижний и верхний
            query = select(ProductsOrm).filter(ProductsOrm.name.ilike(f'%{name}%'))
            result = await session.execute(query)
            return result.scalar()
