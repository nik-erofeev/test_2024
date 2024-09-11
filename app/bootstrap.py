from punq import Container, Scope

from app.repositories.task_repository import TaskRepo
from app.routers.task_router import TaskRouter
from app.services.task_service import TasksServie
from app.settings import AppConfig
from app.utils.db import Db, DbConfig


def bootstrap(app_config: AppConfig) -> Container:
    container = Container()
    container.register(AppConfig, instance=app_config)
    container.register(DbConfig, instance=app_config.bd, scope=Scope.singleton)
    container.register(Db, Db, scope=Scope.singleton)

    container.register(TaskRepo)
    container.register(TasksServie)
    container.register(TaskRouter)

    return container