from contextlib import asynccontextmanager
from pathlib import Path
from loguru import logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from libs.domain.utils import app_exception_handler

from libs.domain.errors.base import BaseApplicationException

from libs.infrastructure.factories.common import ApplicationConfigFactory

from .src.infrastructure.utils import run_migrations

from .src.interface.api.routes import (
    offer_router,
    partner_router,
)


SERVICE_DIR = Path(__file__).parent


# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     logger.info("Starting migrations")
#     try:
#         run_migrations(SERVICE_DIR)
#     except Exception as err:
#         logger.error(err)
#     yield


def create_app() -> FastAPI:
    config = ApplicationConfigFactory.create(
        service_dir=SERVICE_DIR,
    )

    app = FastAPI(
        # lifespan=lifespan,
        **config.openai,
    )

    app.add_exception_handler(
        BaseApplicationException,
        app_exception_handler,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
    )

    [
        app.include_router(route, prefix="/api")
        for route in (offer_router, partner_router)
    ]

    return app


def main():
    run(
        create_app(),
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()
