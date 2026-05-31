# packages

from typing import (
    Any,
    Sequence,
    AsyncGenerator,
)

from sqlalchemy import (
    Executable,
    Result,
)

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.engine import ScalarResult

from contextlib import asynccontextmanager

# application dependencies

from .engine import BaseSQLEngine


class BaseSQLExecutor:
    def __init__(
        self,
        *,
        engine: BaseSQLEngine,
    ) -> None:
        self._engine = engine

    @asynccontextmanager
    async def __open_session(
        self,
    ) -> AsyncGenerator[AsyncSession, None]:
        try:
            async with self._engine.session_factory() as session:
                yield session
        except SQLAlchemyError as err:
            raise RuntimeError(err)
        finally:
            await session.close()

    async def __fetch_scalars(
        self,
        query: Executable,
    ) -> ScalarResult[Any]:
        async with self.__open_session() as session:
            result: Result[Any] = await session.execute(
                query,
            )
            return result.scalars()

    async def _fetch(
        self,
        query: Executable,
        *,
        many: bool,
    ) -> Sequence[Any] | Any | None:
        scalars: ScalarResult[Any] = await self.__fetch_scalars(
            query,
        )
        return scalars.all() if many else scalars.first()

    async def _commit(
        self,
        query: Executable,
    ) -> Result[Any]:
        async with self.__open_session() as session:
            result: Result[Any] = await session.execute(
                query,
            )
            await session.commit()

            return result
