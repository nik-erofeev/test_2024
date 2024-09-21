from punq import Container, Scope

from app.repositories.product_repository import ProductRepo
from app.repositories.task_repository import TaskRepo
from app.repositories.user_repository import UserRepo
from app.routers.login_router import AuthRouter
from app.routers.product_router import ProductRouter
from app.routers.task_router import TaskRouter
from app.routers.user_router import UserRouter
from app.services.product_service import ProductService
from app.services.task_service import TasksServie
from app.services.user_service import UserService
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

    container.register(ProductRepo)
    container.register(ProductService)
    container.register(ProductRouter)

    container.register(UserRepo)
    container.register(UserService)
    container.register(UserRouter)

    container.register(AuthRouter)

    return container
