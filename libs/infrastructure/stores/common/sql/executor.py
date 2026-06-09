# packages

from typing import (
    Any,
    TypeVar,
    Callable,
    Awaitable,
    Sequence,
    AsyncGenerator,
)

from sqlalchemy import (
    # types
    Executable,
    Result,
)

from loguru import logger

from contextlib import (
    nullcontext,
    asynccontextmanager,
)

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.engine import ScalarResult

# application dependencies

from .engine import BaseSQLEngine

from libs.domain.errors.stores import (
    ObjectNotFoundException,
    QueryExecutionException,
)

from libs.domain.utils import orm_model_dump

from libs.domain.errors.stores import RepositoryException


T = TypeVar("T")


class BaseSQLExecutor:
    def __init__(
        self,
        *,
        engine: BaseSQLEngine,
    ) -> None:
        self._engine = engine

    @asynccontextmanager
    async def _session(
        self,
        session: AsyncSession | None = None,
    ) -> AsyncGenerator[AsyncSession, None]:
        try:
            cm = (
                nullcontext(session)
                if session is not None
                else self._engine.session_factory()
            )

            async with cm as session:
                yield session

        except SQLAlchemyError as exc:
            raise RepositoryException from exc

    async def _query(
        self,
        query: Executable,
        *,
        session: AsyncSession | None = None,
    ) -> ScalarResult[Any]:
        try:
            async with self._session(session) as session:
                result: Result[Any] = await session.execute(
                    query,
                )

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

    async def _transaction(
        self,
        action: Callable[[AsyncSession], Awaitable[T]],
        *,
        session: AsyncSession | None = None,
    ) -> T:
        owns_session = session is None

        async with self._session(session) as opened_session:
            try:
                result = await action(opened_session)

                if owns_session:
                    await opened_session.commit()

                return result

            except SQLAlchemyError:
                if owns_session:
                    await opened_session.rollback()

                logger.exception(
                    "Transaction failed",
                    extra={
                        "table": self._table.__name__,
                    },
                )

                raise QueryExecutionException(
                    table=self._table.__name__,
                )

    async def _fetch_one(
        self,
        query: Executable,
        *,
        id: int | None = None,
        session: AsyncSession | None = None,
    ) -> Any:

        result = (
            await self._query(
                query,
                session=session,
            )
        ).first()

        if result is None:
            raise ObjectNotFoundException(
                table=self._table.__name__,
                id=id,
            )

        return result

    async def _fetch_many(
        self,
        query: Executable,
        *,
        session: AsyncSession | None = None,
    ) -> Sequence[Any]:
        return (
            await self._query(
                query,
                session=session,
            )
        ).all()

    async def _before_commit(
        self,
        entity: Any,
        data: Any,
        session: AsyncSession,
    ) -> None:
        pass

    async def _after_commit(
        self,
        entity: Any,
    ) -> Any:
        return entity

    async def _insert(
        self,
        data: Any,
        *,
        session: AsyncSession | None = None,
    ) -> Any:
        async def action(
            opened_session: AsyncSession,
        ) -> Any:
            entity = self._table(
                **orm_model_dump(
                    data,
                    table=self._table.__table__,
                ),
            )

            await self._before_commit(
                entity=entity,
                data=data,
                session=opened_session,
            )

            opened_session.add(entity)

            await opened_session.flush()

            return await self._after_commit(
                entity=entity,
            )

        return await self._transaction(
            action,
            session=session,
        )

    async def _update(
        self,
        id: int,
        data: Any,
        *,
        session: AsyncSession | None = None,
    ) -> Any:
        async def action(
            opened_session: AsyncSession,
        ) -> Any:
            entity = await self.fetch_one(
                id=id,
                session=opened_session,
            )

            for field, value in data.dump.items():
                setattr(entity, field, value)

            await self._before_commit(
                entity=entity,
                data=data,
                session=opened_session,
            )

            await opened_session.flush()

            return await self._after_commit(
                entity=entity,
            )

        return await self._transaction(
            action,
            session=session,
        )

    async def _delete(
        self,
        id: int,
        *,
        session: AsyncSession | None = None,
    ) -> None:
        async def action(
            opened_session: AsyncSession,
        ) -> None:
            entity = await self._fetch_for_update(
                id=id,
                session=opened_session,
            )

            await opened_session.delete(
                entity,
            )

        await self._transaction(
            action,
            session=session,
        )
