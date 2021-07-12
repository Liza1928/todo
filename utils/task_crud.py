from models.tasks import Task_Pydantic, TaskIn_Pydantic, Tasks


async def get_tasks():
    return await Task_Pydantic.from_queryset(Tasks.all())


async def get_task(task_id: int):
    return await Task_Pydantic.from_queryset_single(Tasks.get(id=task_id))


async def create_task(task: TaskIn_Pydantic):
    task_obj = await Tasks.create(**task.dict())
    return await Task_Pydantic.from_tortoise_orm(task_obj)


async def update_task(task_id: int, task: TaskIn_Pydantic):
    await Tasks.filter(id=task_id).update(**task.dict(exclude_unset=True))
    return await Task_Pydantic.from_queryset_single(Tasks.get(id=task_id))


async def delete_task(task_id: int):
    deleted_count = await Tasks.filter(id=task_id).delete()
    return deleted_count


async def clone_repeated():
    repeated_tasks = await Tasks.filter(repeat=True)
    for task in repeated_tasks:
        new_task = await Tasks.create(text=task.text, repeat=task.repeat)
        await new_task.save()
