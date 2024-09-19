import logging

from fastapi import FastAPI

from app.routers.login_handler import AuthRouter
from app.routers.product_router import ProductRouter
from app.routers.task_router import TaskRouter
from app.routers.user_router import UserRouter
from app.settings import AppConfig
from app.utils.db import Db


logger = logging.getLogger(__name__)


class Application:
    def __init__(
        self,
        config: AppConfig,
        db: Db,
        tasks: TaskRouter,
        product: ProductRouter,
        user: UserRouter,
        auth: AuthRouter,
    ):
        self._config = config
        self._db = db
        self._tasks = tasks
        self._product = product
        self._user = user
        self._auth = auth

    def setup(self, server: FastAPI) -> None:
        @server.on_event("startup")
        async def on_startup() -> None:
            await self._db.start()

        @server.on_event("shutdown")
        async def on_shutdown() -> None:
            await self._db.shutdown()

        server.include_router(self._tasks.api_route, prefix="/tasks", tags=["Таски"])
        server.include_router(self._product.api_route, prefix="/products", tags=["Продукты"])
        server.include_router(self._user.api_route, prefix="/users", tags=["Пользователи"])
        server.include_router(self._auth.api_route, prefix="/login", tags=["login"])

    @property
    def app(self) -> FastAPI:
        server = FastAPI(
            title="Test project",
            description="тестовый проект",
            version="8.0.8",
            contact={
                "name": "Nik",
                "email": "erofeev.nik.it@yandex.ru",
            },
            license_info={"name": "TEST_license"},
        )
        self.setup(server)
        return server
