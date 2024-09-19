from uuid import UUID

from sqlalchemy import select, update
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
                if 'unique constraint' in str(e.orig):
                    if 'users_username_key' in str(e.orig):
                        raise ValueError(f"Пользователь с username: {user.username} уже зарегистрирован")
                    elif 'users_email_key' in str(e.orig):
                        raise ValueError(f"Пользователь с email: {user.email} уже зарегистрирован")
                else:
                    # Для всех других случаев, повторно выбрасываем исключение
                    raise
            return user_model

    async def get_user_by_id(self, user_id: UUID):
        async with self._db.get_session() as session:
            query = select(User).filter_by(id=user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str):
        async with self._db.get_session() as session:
            query = select(User).filter_by(email=email)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def delete_user(self, user_id: UUID):
        async with self._db.get_session() as session:
            await session.execute(update(User).where(User.id == user_id).values(is_active=False))
            await session.commit()
