import logging

from app.models.tast import ResponseTaskAdd, STask, STaskAdd
from app.repositories.task_repository import TaskRepo


logger = logging.getLogger(__name__)


class TasksServie:
    def __init__(self, task_repo: TaskRepo):
        self._task_repo = task_repo

    async def create_task(self, task: STaskAdd) -> ResponseTaskAdd:
        try:
            result = await self._task_repo.add_task(task)
            task = STask.model_validate(result)
            return ResponseTaskAdd(task_id=task.task_id, id=task.id)

        except Exception as e:
            logger.warning(f"Exception Error as {e}")

    async def find_all(self) -> STask | None:
        result = await self._task_repo.get_all_tasks()
        if result is None:
            return None

        return [STask.model_validate(task) for task in result]

    async def find_task_by_id(self, task_id: int) -> STask | None:
        task = await self._task_repo.get_task_by_id(task_id)
        if task is None:
            return None

        return STask.model_validate(task)
