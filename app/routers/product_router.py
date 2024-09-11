import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from app.models.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService


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
            status_code=202,
        )
        async def add_product(product: ProductCreate):
            try:
                return await self._product_service.create_product(product)
            except Exception:
                raise HTTPException(status_code=404, detail="Failed to update")

        @router.get(
            '/{product_name}',
            response_model=ProductResponse,
            response_class=ORJSONResponse,
            status_code=200,
        )
        async def get_product_by_name(product_name: str):

            product = await self._product_service.get_product(product_name)

            if product is None:
                raise HTTPException(status_code=404, detail=f"Продукт {product_name} не найден")

            return product
