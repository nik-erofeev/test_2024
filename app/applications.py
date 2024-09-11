import logging

from fastapi import FastAPI

from app.routers.task_router import TaskRouter
from app.settings import AppConfig
from app.utils.db import Db


logger = logging.getLogger(__name__)


class Application:
    def __init__(
        self,
        config: AppConfig,
        tasks: TaskRouter,
        db: Db,
    ):
        self._config = config
        self._db = db
        self._tasks = tasks

    def setup(self, server: FastAPI) -> None:
        @server.on_event("startup")
        async def on_startup() -> None:
            await self._db.start()

        @server.on_event("shutdown")
        async def on_shutdown() -> None:
            await self._db.shutdown()

        server.include_router(self._tasks.api_route, prefix="/tasks", tags=["Таски"])

    @property
    def app(self) -> FastAPI:
        server = FastAPI()
        self.setup(server)
        return server
