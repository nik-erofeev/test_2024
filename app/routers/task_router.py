import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from app.models.tast import ResponseTaskAdd, STask, STaskAdd
from app.services.task_service import TasksServie


logger = logging.getLogger(__name__)


class TaskRouter:
    def __init__(self, task_service: TasksServie):
        self._task_service = task_service

    @property
    def api_route(self) -> APIRouter:
        router = APIRouter()
        self._register(router)
        return router

    def _register(self, router: APIRouter):
        @router.post(
            "/",
            response_model=ResponseTaskAdd,
            response_class=ORJSONResponse,
            status_code=202,
        )
        async def add_tasks(task: Annotated[STaskAdd, Depends()]) -> ResponseTaskAdd:
            try:
                return await self._task_service.create_task(task)

            except Exception:

                raise HTTPException(status_code=404, detail="Failed to update")

        @router.get(
            "/",
            response_class=ORJSONResponse,
            response_model=list[STask],
            status_code=200,
        )
        async def get_tasks() -> list[STask] | None:

            tasks = await self._task_service.find_all()
            if tasks is None:
                raise HTTPException(status_code=404, detail="Таски не найдены")

            return tasks

        @router.get(
            "/{task_id}",
            response_class=ORJSONResponse,
            response_model=STask,
            status_code=200,
        )
        async def task_by_id(task_id: int):
            task = await self._task_service.find_task_by_id(task_id)

            if task is None:
                raise HTTPException(status_code=404, detail={f"Таска {task_id} не найдена"})

            return task
