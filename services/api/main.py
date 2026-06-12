# packages

from uvicorn import run

from pathlib import Path

from loguru import logger

from fastapi import FastAPI

from contextlib import asynccontextmanager

from fastapi_pagination import add_pagination

from fastapi.middleware.cors import CORSMiddleware


# application dependencies

from .src.interface.api.routes import (
    offer_router,
    partner_router,
    link_router,
    offer_position_router,
)

from libs.domain.types.enums.config import AppMode

from libs.domain.utils.exception_handler import app_exception_handler

from .src.interface.routing import ApplicationRouter

from libs.domain.errors.base import BaseApplicationException

from .src.infrastructure.utils.functions import run_migrations

from libs.infrastructure.factories.common import ApplicationConfigFactory


SERVICE_DIR = Path(__file__).parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Starting migrations")
    try:
        run_migrations(SERVICE_DIR)
    except Exception as err:
        logger.error(err)
    yield


def create_app() -> FastAPI:
    config = ApplicationConfigFactory.create(
        service_dir=SERVICE_DIR,
    )

    app = FastAPI(
        lifespan=lifespan if config.mode == AppMode.PRODUCTION else None,
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

    ApplicationRouter(
        app=app,
    ).register_routes(
        routes=[
            offer_router,
            partner_router,
            link_router,
            offer_position_router,
        ]
    )

    add_pagination(app)

    return app


def main():
    run(
        create_app(),
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()
