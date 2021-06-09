import asyncio
import logging
import os

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from configs.db import DB_CONFIG
from models.tasks import Tasks
from routers import tasks

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(tasks.router)
    return application


app = create_application()
register_tortoise(
    app,
    config=DB_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.on_event("startup")
async def startup_event():
    print("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


@app.get("/")
async def root():
    return {"message": "Hello, this is fast-api todo application"}
