import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.models.product import (
    ProductCreate,
    ProductDeleteResponse,
    ProductResponse,
    ProductUpdate,
    ProductUpdateResponse,
)
from app.repositories.product_repository import ProductRepo
from app.utils.pagination import PaginationParams


logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, product_repo: ProductRepo):
        self._product_repo = product_repo

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        try:
            result = await self._product_repo.add_product(product)

        except SQLAlchemyError as e:
            logger.exception(f"Database error occurred while adding product, {e}")
            raise HTTPException(status_code=500, detail="Database error occurred")

        except ValueError as value_error:
            logger.exception("Invalid data provided for product creation.")
            raise HTTPException(status_code=400, detail=str(value_error))

        return ProductResponse.model_validate(result)

    async def get_product_by_id(self, product_id: UUID) -> ProductResponse | None:
        product = await self._product_repo.get_product_id(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail=f"Продукт product_id: {product_id} не найден")

        return ProductResponse.model_validate(product)

    async def get_product_pagination(self, pagination: PaginationParams) -> list[ProductResponse]:
        try:
            products = await self._product_repo.get_product_pagination(pagination.page, pagination.per_page)
            return [ProductResponse.model_validate(product) for product in products]
        except SQLAlchemyError as e:
            logger.exception(f"Database error occurred while retrieving products, {e}")
            raise HTTPException(status_code=500, detail="Database error occurred")

    async def update_product_by_id(
        self,
        product_id: UUID,
        product_update: ProductUpdate,
    ) -> ProductUpdateResponse:
        try:
            await self.get_product_by_id(product_id)

            update_success = await self._product_repo.update_product(product_id, product_update)
            if not update_success:
                raise HTTPException(status_code=404, detail="Никакие изменения не были внесены")

            return ProductUpdateResponse(product_id=product_id, message="Успешно обновлен")

        except SQLAlchemyError as e:
            logger.exception("Database error occurred while updating product")
            raise e

    async def delete_product_by_id(self, product_id: UUID) -> ProductDeleteResponse:
        try:
            await self.get_product_by_id(product_id)
            await self._product_repo.delete_product(product_id)

            return ProductDeleteResponse(id=product_id, message="Успешно удален")
        except SQLAlchemyError as e:
            logger.exception("Database error occurred while updating product")
            raise e
