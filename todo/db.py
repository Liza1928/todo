from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


def get_db_uri(user, passwd, host, db):
    return f"postgres://{user}:{passwd}@{host}:5433/{db}"


TORTOISE_ORM = {
    "connections": {"default": get_db_uri(
            user="todo",
            passwd="password",
            host="127.0.0.1",
            db="todo"
        )},
    "apps": {
        "models": {
            "models": ["todo.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=get_db_uri(
            user="todo",
            passwd="password",
            host="127.0.0.1",
            db="todo"
        ),
        modules={"models": ["todo.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )