import logging
import os

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
import aioredis

from configs.db import DB_CONFIG
from models.admin import Admin
from routers import tasks
from constants import BASE_DIR
from settings import REDIS_PASSWORD, REDIS_URL
import admin

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI()
    application.mount(
        "/static",
        StaticFiles(directory=os.path.join(BASE_DIR, "static")),
        name="static",
    )

    @application.on_event("startup")
    async def startup():
        redis = await aioredis.create_redis_pool(
            REDIS_URL, encoding="utf8", password=REDIS_PASSWORD)
        application.include_router(tasks.router)
        login_provider = UsernamePasswordProvider(
            admin_model=Admin,
            login_logo_url="https://preview.tabler.io/static/logo.svg"
        )
        await admin_app.configure(
            logo_url="https://preview.tabler.io/static/logo-white.svg",
            template_folders=[os.path.join(BASE_DIR, "templates")],
            providers=[login_provider],
            redis=redis,
        )

    application.mount("/admin", admin_app)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    register_tortoise(
        application,
        config=DB_CONFIG,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    return application


app = create_application()

security = HTTPBasic()


@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


@app.get("/")
async def root():
    return {"message": "Hello, this is fast-api todo application"}