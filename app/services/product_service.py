import logging

from sqlalchemy.exc import SQLAlchemyError

from app.models.product import ProductCreate, ProductResponse
from app.repositories.product_repository import ProductRepo


logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, product_repo: ProductRepo):
        self._product_repo = product_repo

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        try:
            result = await self._product_repo.add_product(product)
        except SQLAlchemyError as e:
            logger.exception("Database error occurred while adding product")
            raise e
        except ValueError as value_error:
            logger.exception("Invalid data provided for product creation.")
            raise value_error

        return ProductResponse.model_validate(result)

    async def get_product(self, name: str) -> ProductResponse | None:
        product = await self._product_repo.get_product_by_name(name.lower())
        if product is None:
            return None
        return ProductResponse.model_validate(product)
