import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["todo.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["todo.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )