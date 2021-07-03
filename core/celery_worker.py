import asyncio

from tortoise import Tortoise
from celery.schedules import crontab

from core.celery_app import celery_app
from utils import task_crud
from settings import DATABASE_URL


@celery_app.on_after_configure.connect
def setup_repeated_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(hour=0, minite=0),
        create_repeated_task.s()
    )


async def create_repeated_tasks_async():
    """Не подхватывает модель базы без принудительной инициализации"""
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["models"]})
    await Tortoise.generate_schemas()
    return await task_crud.clone_repeated()


@celery_app.task
def create_repeated_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_repeated_tasks_async())


