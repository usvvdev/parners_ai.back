# packges

from typing import Any

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

# application dependencies

from ..models import UtmSources

from ..repository import MySQLRepository


class UTMSourceRepository(MySQLRepository[UtmSources]):
    _table: type[UtmSources] = UtmSources

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            table=self._table,
            *args,
            **kwargs,
        )

    async def fetch_one(
        self,
        id: int,
        session: AsyncSession | None = None,
    ) -> type[UtmSources] | None:
        return await self._fetch_one(
            id=id,
            session=session,
        )

    async def fetch_many(
        self,
        session: AsyncSession | None = None,
    ) -> type[UtmSources] | None:
        return await self._fetch_many(
            query=select(
                self._table,
            ),
            session=session,
        )

    async def insert(
        self,
        data: Any,
        session: AsyncSession | None = None,
    ) -> type[UtmSources]:
        return await self._insert(
            data=data,
            session=session,
        )

    async def update(
        self,
        id: int,
        data: Any,
        *,
        session: AsyncSession | None = None,
    ) -> type[UtmSources]:
        return await self._update(
            id=id,
            data=data,
            session=session,
        )

    async def delete(
        self,
        id: int,
        *,
        session: AsyncSession | None = None,
    ) -> None:
        await self._delete(
            id=id,
            session=session,
        )
