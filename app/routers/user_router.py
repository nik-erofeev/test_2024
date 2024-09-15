import logging

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.models.user import UserCreate, UserResponse
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
            response_model=UserResponse,
            response_class=ORJSONResponse,
            status_code=201,
        )
        async def create_new_user(user: UserCreate):
            return await self._user_service.create_user(user)
