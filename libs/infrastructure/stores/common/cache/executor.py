# packages

from typing import (
    Any,
    Callable,
    Awaitable,
    AsyncGenerator,
)

from contextlib import asynccontextmanager

# application dependencies

from .engine import BaseCacheEngine


class BaseCacheExecutor:
    def __init__(
        self,
        *,
        engine: BaseCacheEngine,
    ) -> None:
        self._engine = engine

    @asynccontextmanager
    async def __open_connection(self) -> AsyncGenerator[Any, None]:
        try:
            redis = self._engine.engine
            yield redis
        except Exception as err:
            raise RuntimeError(err)

    async def _execute(
        self,
        func: Callable[..., Awaitable[Any]],
        *args,
        **kwargs,
    ) -> Callable[..., Awaitable[Any]]:
        async with self.__open_connection() as redis:
            return await func(
                redis,
                *args,
                **kwargs,
            )
