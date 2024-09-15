from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 5


PaginationDep = Annotated[PaginationParams, Depends()]
