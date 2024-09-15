import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepo


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repo: UserRepo) -> UserResponse:
        self._user_repo = user_repo

    async def create_user(self, user: UserCreate):
        try:
            await self._user_repo.add_user(user)

            return UserResponse(
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
