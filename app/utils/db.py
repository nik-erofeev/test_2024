import contextlib
import logging
from collections.abc import AsyncIterator

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr


logger = logging.getLogger(__name__)


class DbConfig(BaseModel):
    dsn: str
    max_size: int = 1
    min_size: int = 1
    statement_cache_size: int = 1024 * 15


class Base(DeclarativeBase):
    """Базовая модель"""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def __repr__(self):
        """
        Печать орм-объектов с отображением атрибутов
        """

        fmt = "{}.{}({})"
        package = self.__class__.__module__
        class_ = self.__class__.__name__
        attrs = sorted((k, getattr(self, k)) for k in self.__mapper__.columns.keys())
        sattrs = ", ".join("{}={!r}".format(*x) for x in attrs)
        return fmt.format(package, class_, sattrs)


class Db:
    def __init__(self, config: DbConfig):
        self._config = config
        self._engine = create_async_engine(
            url=config.dsn,
            echo=True,
            pool_size=config.max_size,
            max_overflow=10,  # Настройки пула соединений
        )

        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)

    async def _create_table(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def _delete_table(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    # async def get_session(self) -> AsyncIterator[AsyncSession]:  # todo: в repo todo
    #     async with self._sessionmaker() as session:
    #         try:
    #             yield session
    #         except Exception as exc:
    #             await session.rollback()
    #             raise exc
    #         else:
    #             await session.commit()

    # async def get_session(self) -> AsyncSession:
    #     return self._sessionmaker()

    @contextlib.asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """
        Асинхронный контекстный менеджер для работы с сессией.
        """
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception as exc:
                await session.rollback()
                raise exc
            else:
                await session.commit()

    async def start(self):
        logger.info("Initializing database connection...")
        # await self._delete_table()  # Очистка БД перед стартом
        # await self._create_table()  # Создание новых таблиц в БД
        async with self._engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection initialized successfully.")

    async def shutdown(self):
        logger.info("Shutting down database connection...")
        await self._engine.dispose()
