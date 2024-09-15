import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.models.user import UserCreate, UserCreateResponse, UserDelResponse, UserResponse
from app.services.user_service import UserService


logger = logging.getLogger(__name__)


class UserRouter:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    @property
    def api_route(self) -> APIRouter:
        router = APIRouter()
        self._register(router)
        return router

    def _register(self, router: APIRouter):
        @router.post(
            "/",
            response_model=UserCreateResponse,
            response_class=ORJSONResponse,
            status_code=201,
        )
        async def create_new_user(user: UserCreate):
            return await self._user_service.create_user(user)

        @router.get(
            "/",
            response_model=UserResponse,
            response_class=ORJSONResponse,
            status_code=200,
        )
        async def get_user_by_id(user_id: UUID):
            return await self._user_service.get_user_by_id(user_id)

        @router.delete(
            "/",
            response_model=UserDelResponse,
            response_class=ORJSONResponse,
            status_code=201,
        )
        async def delete_user(user_id: UUID):
            return await self._user_service.delete_user_by_id(user_id)
