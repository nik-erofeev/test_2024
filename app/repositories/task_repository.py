from sqlalchemy import select

from app.models.tast import STaskAdd
from app.orm_models import Task
from app.utils.db import Db


class TaskRepo:
    def __init__(self, db: Db):
        self._db = db

    async def add_task(self, data: STaskAdd) -> Task:
        # async for session in self._db.get_session():  # todo если через итератор сессий в БД
        async with self._db.get_session() as session:
            task_dict = data.model_dump()

            task = Task(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task

    async def get_all_tasks(self) -> list[Task]:
        # async for session in self._db.get_session():  # todo если через итератор сессий в БД
        async with self._db.get_session() as session:
            query = select(Task)
            result = await session.execute(query)
            task_models = result.scalars().all()
            return task_models

    async def get_task_by_id(self, task_id: int) -> Task | None:
        # async for session in self._db.get_session():  # todo если через итератор сессий в БД
        async with self._db.get_session() as session:
            query = select(Task).filter_by(task_id=task_id)
            # query = select(TasksOrm).filter(TasksOrm.task_id == task_id)
            result = await session.execute(query)
            task = result.scalar()
            return task
