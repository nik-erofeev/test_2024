import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import UserCreate, UserCreateResponse, UserDelResponse, UserResponse, UserResponseAll, UserUpdate
from app.orm_models import User
from app.repositories.user_repository import UserRepo
from app.settings import configure_logging
from app.utils.hasher import Hasher


logger = logging.getLogger(__name__)
configure_logging(level=logging.INFO)


class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self._user_repo = user_repo

    async def create_user(self, user: UserCreate):
        try:

            hashed_password = Hasher.get_password_hash(user.hashed_password)

            new_user = UserCreate(username=user.username, email=user.email, hashed_password=hashed_password)
            await self._user_repo.add_user(new_user)

            return UserCreateResponse(
                username=user.username,
                email=user.email,
                message="Зарегистрирован",
            )

        except ValueError as e:
            logger.warning(f"User creation failed: {e}")
            raise HTTPException(status_code=404, detail=str(e))

        except SQLAlchemyError as e:
            logger.exception(f"Database error occurred while adding product, {e}")
            raise HTTPException(status_code=500, detail="Database error occurred")

    async def get_user_by_id(self, user_uuid: UUID) -> UserResponse:
        user = await self._user_repo.get_user_by_uuid(user_uuid)
        if user is None:
            raise HTTPException(status_code=404, detail=f"Пользователь user_id: {user_uuid} не найден")

        if not user.is_active:
            raise HTTPException(status_code=404, detail=f"Пользователь user_id: {user_uuid} деактивирован/удален")

        return UserResponse.model_validate(user)

    async def get_user_by_email(self, email: str) -> UserResponseAll:
        user = await self._user_repo.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail=f"Пользователь с email: {email} не найден")

        return UserResponseAll.model_validate(user)

    async def get_user_by_username(self, username: str) -> UserResponseAll:
        user = await self._user_repo.get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=404, detail=f"Пользователь с username: {username} не найден")

        return UserResponseAll.model_validate(user)

    async def delete_user_by_id(self, user_id: UUID) -> UserDelResponse:
        try:
            await self._user_repo.delete_user(user_id)
            return UserDelResponse(id=user_id, message="Пользователь удален")
        except SQLAlchemyError as e:
            logger.exception("Database error occurred while updating product")
            raise e

    async def update_user_by_uuid(self, user_uuid: UUID, user_update: UserUpdate) -> UserResponse:
        user: User | None = await self._user_repo.get_user_by_uuid(user_uuid)
        if user is None:
            raise HTTPException(status_code=404, detail=f"Пользователь с id: {user_uuid} не найден")

        if not user.is_active:
            raise HTTPException(
                status_code=403,
                detail=f"Пользователь с id: {user_uuid} удален и не может быть обновлен",
            )

        try:
            updated_user = await self._user_repo.update_user(user_uuid, user_update)
            return UserResponse.model_validate(updated_user)
        except ValueError as e:
            logger.warning(f"User update failed: {e}")
            raise HTTPException(status_code=400, detail=str(e))
