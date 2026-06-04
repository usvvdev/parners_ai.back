# packages

from typing import (
    Any,
    Generic,
)

from sqlalchemy import (
    # functions,
    select,
    insert,
    update,
    delete,
    # types,
    Select,
    Insert,
    Update,
    Delete,
)

from sqlalchemy.ext.asyncio import AsyncSession

# application dependencies

from ..base import TTable

from .engine import BaseSQLEngine

from .executor import BaseSQLExecutor


class BaseSQLRepository(
    BaseSQLExecutor,
    Generic[TTable],
):
    def __init__(
        self,
        *,
        engine: BaseSQLEngine,
        table: type[TTable],
    ) -> None:
        super().__init__(
            engine=engine,
        )
        self._table = table

    async def fetch(
        self,
        query: Select | None = None,
        *,
        many: bool = True,
        session: AsyncSession | None = None,
        **kwargs,
    ) -> list[TTable] | TTable | None:
        stmt: Select = query if query is not None else select(self._table)
        return await self._fetch(
            stmt,
            many=many,
            session=session,
            **kwargs,
        )

    async def insert(
        self,
        data: Any,
    ) -> TTable:
        stmt: Insert = insert(self._table).values(
            **data.dump,
        )
        return await self._commit(
            stmt,
        )

    async def update(
        self,
        *,
        id: int,
        data: dict[str, Any],
    ) -> TTable | None:
        stmt: Update = (
            update(self._table)
            .filter_by(id=id)
            .values(
                **data,
            )
        )
        return await self._commit(
            stmt,
        )

    async def delete(
        self,
        *,
        id: int,
    ) -> TTable | None:
        stmt: Delete = delete(self._table).filter_by(id=id)
        return await self._commit(
            stmt,
        )
