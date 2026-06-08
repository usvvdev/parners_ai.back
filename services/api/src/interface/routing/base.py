from fastapi import (
    FastAPI,
    APIRouter,
)


class ApplicationRouter:
    def __init__(
        self,
        app: FastAPI,
    ) -> None:
        self._app = app

    def register_routes(
        self,
        prefix: str = "/api",
        *,
        routes: list[APIRouter],
    ) -> None:
        for route in routes:
            self._app.include_router(
                route,
                prefix=prefix,
            )
