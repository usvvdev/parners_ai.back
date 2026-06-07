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
    Partners,
    Links,
)

from ..repository import MySQLRepository


class PartnerRepository(MySQLRepository[Partners]):
    _table: type[Partners] = Partners

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

    async def __fetch_links(
        self,
        session: AsyncSession,
        link_ids: list[int] = [],
    ) -> list[Links]:
        return await self._fetch_many(
            query=select(Links).where(
                Links.id.in_(link_ids),
            ),
            session=session,
        )

    async def __commit_links(
        self,
        entity: Partners,
        session: AsyncSession,
        link_ids: list[int] | None,
    ) -> None:
        if link_ids is None:
            return

        entity.links = await self.__fetch_links(
            session=session,
            offer_ids=link_ids,
        )

    async def _before_commit(
        self,
        entity: Links,
        data: Any,
        session: AsyncSession,
    ) -> None:
        await self.__commit_links(
            entity=entity,
            session=session,
            link_ids=data.link_ids,
        )

    async def _after_commit(
        self,
        entity: Partners,
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
    ) -> Optional[Partners]:
        return await self._fetch_one(
            query=select(self._table)
            .options(
                selectinload(self._table.links),
            )
            .where(self._table.id == id),
            id=id,
            session=session,
        )

    async def fetch_many(
        self,
        session: AsyncSession | None = None,
    ) -> type[Partners] | None:
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
    ) -> Partners:
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
    ) -> Partners:
        partner = await self.fetch_one(
            id=id,
            session=session,
        )
        return await self._update(
            partner,
            data=data,
            session=session,
        )

    async def delete(
        self,
        id: int,
        *,
        session: AsyncSession | None = None,
    ) -> None:
        partner: type[Links] | None = await self.fetch_one(
            id=id,
            session=session,
        )
        await self._delete(
            partner,
            session=session,
        )
