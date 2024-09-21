from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.user import UserCreate, UserUpdate
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

    async def get_user_by_uuid(self, user_uuid: UUID) -> User | None:
        async with self._db.get_session() as session:
            query = select(User).filter_by(id=user_uuid)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        async with self._db.get_session() as session:
            query = select(User).filter_by(email=email)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        async with self._db.get_session() as session:
            query = select(User).filter_by(username=username)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def delete_user(self, user_id: UUID):
        async with self._db.get_session() as session:
            await session.execute(update(User).where(User.id == user_id).values(is_active=False))
            await session.commit()

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> User | None:
        async with self._db.get_session() as session:

            query = (
                update(User)
                .where(User.id == user_id)
                .values(**user_update.model_dump(exclude_unset=True))
                .returning(User)
            )
            try:
                result = await session.execute(query)
                await session.commit()
                updated_user = result.scalars().first()
                if updated_user:
                    return updated_user
                else:
                    raise ValueError(f"Пользователь с id: {user_id} не найден")
            except IntegrityError as e:
                if 'unique constraint' in str(e.orig):
                    if 'users_username_key' in str(e.orig):
                        raise ValueError(f"Пользователь с username: {user_update.username} уже зарегистрирован")
                    elif 'users_email_key' in str(e.orig):
                        raise ValueError(f"Пользователь с email: {user_update.email} уже зарегистрирован")
                else:
                    # Для всех других случаев, повторно выбрасываем исключение
                    raise
            except SQLAlchemyError as e:
                raise e
