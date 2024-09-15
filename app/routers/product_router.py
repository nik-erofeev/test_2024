import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.models.product import (
    ProductCreate,
    ProductDeleteResponse,
    ProductResponse,
    ProductUpdate,
    ProductUpdateResponse,
)
from app.services.product_service import ProductService
from app.utils.pagination import PaginationDep


logger = logging.getLogger(__name__)


class ProductRouter:
    def __init__(self, product_service: ProductService):
        self._product_service = product_service

    @property
    def api_route(self) -> APIRouter:
        router = APIRouter()
        self._register(router)
        return router

    def _register(self, router: APIRouter):
        @router.post(
            "/",
            response_model=ProductResponse,
            response_class=ORJSONResponse,
            status_code=201,
        )
        async def add_product(product: ProductCreate):
            return await self._product_service.create_product(product)

        @router.get(
            '/{product_id}',
            response_model=ProductResponse,
            response_class=ORJSONResponse,
            status_code=200,
        )
        async def get_product_by_id(product_id: UUID):
            return await self._product_service.get_product_by_id(product_id)

        @router.get(
            '/',
            response_model=list[ProductResponse],
            response_class=ORJSONResponse,
            status_code=200,
        )
        async def get_all_pagination(pagination: PaginationDep):
            return await self._product_service.get_product_pagination(pagination)

        @router.patch(
            "/{product_id}",
            response_model=ProductUpdateResponse,
            response_class=ORJSONResponse,
            status_code=200,
        )
        async def update_product(product_id: UUID, product_update: ProductUpdate):
            return await self._product_service.update_product_by_id(product_id, product_update)

        @router.delete(
            "/{product_id}",
            response_model=ProductDeleteResponse,
            response_class=ORJSONResponse,
            status_code=200,
        )
        async def delete_product(product_id: UUID):
            return await self._product_service.delete_product_by_id(product_id)
