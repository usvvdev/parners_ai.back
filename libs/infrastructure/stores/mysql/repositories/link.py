# packages

from typing import (
    Any,
    Optional,
)

from sqlalchemy import select

from sqlalchemy.orm import selectinload

from sqlalchemy.ext.asyncio import AsyncSession

# application dependencies

from ..models import (
    Links,
    Offers,
)

from ..repository import MySQLRepository


class LinkRepository(MySQLRepository[Links]):
    _table: type[Links] = Links

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

    async def __fetch_offers(
        self,
        session: AsyncSession,
        offer_ids: list[int] = [],
    ) -> list[Offers]:
        return await self._fetch_many(
            query=select(Offers).where(
                Offers.id.in_(offer_ids),
            ),
            session=session,
        )

    async def __commit_offers(
        self,
        entity: Links,
        session: AsyncSession,
        offer_ids: list[int] | None,
    ) -> None:
        if offer_ids is None:
            return

        entity.offers = await self.__fetch_offers(
            session=session,
            offer_ids=offer_ids,
        )

    async def _before_commit(
        self,
        entity: Links,
        data: Any,
        session: AsyncSession,
    ) -> None:
        await self.__commit_offers(
            entity,
            session=session,
            offer_ids=data.offer_ids,
        )

    async def _after_commit(
        self,
        entity: Links,
        session: AsyncSession,
    ) -> Links:
        return await self.fetch_one(
            entity.id,
            session=session,
        )

    async def fetch_one(
        self,
        id: int,
        session: AsyncSession | None = None,
    ) -> Optional[Links]:
        return await self._fetch_one(
            query=select(self._table)
            .options(
                selectinload(self._table.offers),
            )
            .where(self._table.id == id),
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
        *,
        session: AsyncSession | None = None,
    ) -> Links:
        return await self._insert(
            data,
            session=session,
        )

    async def update(
        self,
        id: int,
        data: Any,
        *,
        session: AsyncSession | None = None,
    ) -> Links:
        link = await self.fetch_one(
            id=id,
            session=session,
        )
        return await self._update(
            link,
            data=data,
            session=session,
        )

    async def delete(
        self,
        id: int,
        *,
        session: AsyncSession | None = None,
    ) -> None:
        link: type[Links] | None = await self.fetch_one(
            id=id,
            session=session,
        )
        await self._delete(
            link,
            session=session,
        )
