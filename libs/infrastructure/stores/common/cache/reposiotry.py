# packages

from json import (
    dumps,
    loads,
)

from typing import (
    Any,
    Generic,
)

from redis.asyncio import Redis

# application dependencies

from ..base import TTable

from .engine import BaseCacheEngine

from .executor import BaseCacheExecutor


class BaseCacheRepository(
    BaseCacheExecutor,
    Generic[TTable],
):
    def __init__(
        self,
        *,
        engine: BaseCacheEngine,
        table: type[TTable],
    ) -> None:
        super().__init__(
            engine=engine,
        )
        self._table = table

    async def __generate_key(
        self,
        id: int,
    ) -> str:
        return f"{self._table.__tablename__}:{id}"

    async def get(
        self,
        id: int,
    ) -> dict | None:
        key: str = await self.__generate_key(id)

        async def _get(
            redis: Redis,
            key: str,
        ) -> Any | None:
            value = await redis.get(
                key,
            )
            return loads(value) if value is not None else None

        return await self._execute(
            _get,
            key,
        )

    async def set(
        self,
        id: int,
        value: dict[str, Any],
        *,
        expire: int | None = None,
    ) -> None:
        key: str = await self.__generate_key(id)

        async def _set(
            redis: Redis,
            key: str,
            value: dict[str, Any],
            expire: int | None,
        ) -> None:
            payload: str = dumps(value)

            await redis.set(
                key,
                payload,
                ex=expire,
            )

        await self._execute(
            _set,
            key,
            value,
            expire,
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        key: str = await self.__generate_key(id)

        async def _delete(
            redis: Redis,
            key: str,
        ) -> None:
            await redis.delete(
                key,
            )

        await self._execute(
            _delete,
            key,
        )
