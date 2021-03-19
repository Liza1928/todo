from .routers import tasks

import logging

from .db import init_db
from fastapi import FastAPI

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(tasks.router)
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


@app.get("/")
async def root():
    return {"message": "Hello, this is fast-api todo application"}
