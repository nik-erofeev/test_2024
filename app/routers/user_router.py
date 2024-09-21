import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from app.models.user import UserCreate, UserCreateResponse, UserDelResponse, UserResponse, UserResponseAll, UserUpdate
from app.routers.login_router import oauth2_scheme
from app.services.user_service import UserService
from app.utils.auth import get_current_user_from_token


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
            status_code=status.HTTP_201_CREATED,
        )
        async def create_new_user(user: UserCreate):
            return await self._user_service.create_user(user)

        @router.get(
            "/uuid/{user_uuid}",
            response_model=UserResponse,
            response_class=ORJSONResponse,
            status_code=status.HTTP_200_OK,
        )
        async def get_user_by_id(
            user_uuid: UUID,
            current_user: UserResponseAll = Depends(self._get_current_user),
        ):
            return await self._user_service.get_user_by_id(user_uuid)

        @router.get(
            "/",
            response_model=UserResponse,
            response_class=ORJSONResponse,
            status_code=status.HTTP_200_OK,
        )
        async def get_user_info(
            current_user: UserResponseAll = Depends(self._get_current_user),
        ):
            return await self._user_service.get_user_by_id(current_user.id)

        @router.get(
            "/{username}",
            response_model=UserResponse,
            response_class=ORJSONResponse,
            status_code=status.HTTP_200_OK,
        )
        async def get_user_by_username(
            username: str,
            current_user: UserResponseAll = Depends(self._get_current_user),
        ):
            return await self._user_service.get_user_by_username(username)

        @router.delete(
            "/",
            response_model=UserDelResponse,
            response_class=ORJSONResponse,
            status_code=201,
        )
        async def delete_user(
            current_user: UserResponseAll = Depends(self._get_current_user),
        ):
            return await self._user_service.delete_user_by_id(current_user.id)

        @router.patch(
            '/',
            response_model=UserResponse,
            response_class=ORJSONResponse,
            status_code=status.HTTP_201_CREATED,
        )
        async def update_user(
            user_update: UserUpdate,
            current_user: UserResponseAll = Depends(self._get_current_user),
        ):
            return await self._user_service.update_user_by_uuid(current_user.id, user_update)

    async def _get_current_user(self, token: str = Depends(oauth2_scheme)) -> UserResponseAll:
        return await get_current_user_from_token(token, self._user_service)
