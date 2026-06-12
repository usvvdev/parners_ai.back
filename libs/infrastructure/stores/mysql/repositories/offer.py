# packges

from typing import Any

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

# application dependencies

from ..models import Offers

from ..repository import MySQLRepository


class OfferRepository(MySQLRepository[Offers]):
    _table: type[Offers] = Offers

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
    ) -> type[Offers] | None:
        return await self._fetch_one(
            id=id,
            session=session,
        )

    async def fetch_many(
        self,
        session: AsyncSession | None = None,
    ) -> type[Offers] | None:
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
    ) -> type[Offers]:
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
    ) -> type[Offers]:
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
