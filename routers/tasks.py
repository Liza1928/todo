from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from pydantic import BaseModel
from starlette import status

from utils import task_crud
from models.tasks import Task_Pydantic, TaskIn_Pydantic

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


class Status(BaseModel):
    message: str


@router.get("", response_model=List[Task_Pydantic])
async def get_tasks():
    return await task_crud.get_tasks()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Task_Pydantic)
async def create_task(task: TaskIn_Pydantic):
    return await task_crud.create_task(task)


@router.get(
    "/{task_id}", response_model=Task_Pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_task(task_id: int):
    return await task_crud.get_task(task_id)


@router.put(
    "/{task_id}", response_model=Task_Pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_task(task_id: int, task: TaskIn_Pydantic):
    return await task_crud.update_task(task_id, task)


@router.delete(
    "/{task_id}", response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_task(task_id: int):
    deleted_count = await task_crud.delete_task(task_id)
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return Status(message=f"Deleted task {task_id}")
