from uuid import UUID

from pydantic import BaseModel


class STaskAdd(BaseModel):
    name: str
    description: str | None


class STask(STaskAdd):
    id: UUID
    task_id: int

    class Config:
        from_attributes = True


class ResponseTaskAdd(BaseModel):
    ok: bool = True
    id: UUID
    task_id: int
