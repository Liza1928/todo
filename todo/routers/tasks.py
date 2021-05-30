from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from pydantic import BaseModel
from starlette import status

from todo.models import Task_Pydantic, TaskIn_Pydantic, Tasks

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


class Status(BaseModel):
    message: str


@router.get("", response_model=List[Task_Pydantic])
async def get_tasks():
    return await Task_Pydantic.from_queryset(Tasks.all())


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Task_Pydantic)
async def create_task(task: TaskIn_Pydantic):
    task_obj = await Tasks.create(**task.dict())
    return await Task_Pydantic.from_tortoise_orm(task_obj)


@router.get(
    "/{task_id}", response_model=Task_Pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_task(task_id: int):
    return await Task_Pydantic.from_queryset_single(Tasks.get(id=task_id))


@router.put(
    "/{task_id}", response_model=Task_Pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_task(task_id: int, task: TaskIn_Pydantic):
    await Tasks.filter(id=task_id).update(**task.dict(exclude_unset=True))
    return await Task_Pydantic.from_queryset_single(Tasks.get(id=task_id))


@router.delete(
    "/{task_id}", response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_task(task_id: int):
    deleted_count = await Tasks.filter(id=task_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return Status(message=f"Deleted task {task_id}")
