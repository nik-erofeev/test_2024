from sqlalchemy.exc import IntegrityError

from app.models.user import UserCreate
from app.orm_models import User
from app.utils.db import Db


class UserRepo:
    def __init__(self, db: Db):
        self._db = db

    async def add_user(self, user: UserCreate) -> User:
        async with self._db.get_session() as session:
            user_dict = user.model_dump()

            user_model = User(**user_dict)
            session.add(user_model)
            try:
                await session.flush()
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                if 'unique constraint "users_username_key"' in str(e.orig):
                    raise ValueError(
                        f"Пользователь с email: {user.email} или username: {user.username} уже зарегистрирован",
                    )
                raise
            return user_model
