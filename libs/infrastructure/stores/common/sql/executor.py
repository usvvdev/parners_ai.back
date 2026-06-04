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

from loguru import logger

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.engine import ScalarResult

from contextlib import asynccontextmanager

# application dependencies

from .engine import BaseSQLEngine

from libs.domain.errors.stores import (
    ObjectNotFoundException,
    QueryExecutionException,
)

from libs.domain.errors.stores import RepositoryException


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
        except SQLAlchemyError:
            raise RepositoryException

    async def __fetch_scalars(
        self,
        query: Executable,
        session: AsyncSession | None = None,
    ) -> ScalarResult[Any]:
        try:
            if session is not None:
                result: Result[Any] = await session.execute(query)

            async with self.__open_session() as session:
                result: Result[Any] = await session.execute(query)

            return result.scalars()

        except SQLAlchemyError:
            logger.exception(
                "Failed query execution",
                extra={
                    "table": self._table.__name__,
                    "query": str(query),
                },
            )

            raise QueryExecutionException(
                table=self._table.__name__,
            )

    async def _fetch(
        self,
        query: Executable,
        *,
        many: bool,
        id: int | None = None,
        session: AsyncSession | None = None,
    ) -> Sequence[Any] | Any | None:
        scalars: ScalarResult[Any] = await self.__fetch_scalars(
            query,
            session=session,
        )
        result = scalars.all() if many else scalars.first()

        if not result:
            raise ObjectNotFoundException(
                table=self._table.__name__,
                id=id,
            )

        return result

    async def _commit(
        self,
        query: Executable,
    ) -> Result[Any]:
        async with self.__open_session() as session:
            try:
                result: Result[Any] = await session.execute(query)

                await session.commit()

                return result

            except SQLAlchemyError:
                await session.rollback()

                logger.exception(
                    "Failed query execution",
                    extra={
                        "table": self._table.__name__,
                        "query": str(query),
                    },
                )

                raise QueryExecutionException(
                    table=self._table.__name__,
                )
