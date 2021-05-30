import logging

from fastapi import FastAPI


from todo.db import init_db
from todo.routers import tasks

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(tasks.router)
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


@app.get("/")
async def root():
    return {"message": "Hello, this is fast-api todo application"}
