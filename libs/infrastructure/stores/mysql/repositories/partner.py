# packages

from typing import (
    Any,
    Optional,
)

from sqlalchemy import (
    select,
    desc,
)

from fastapi_pagination import Params

from sqlalchemy.orm import selectinload

from sqlalchemy.ext.asyncio import AsyncSession

# application dependencies

from ..models import (
    Partners,
    Links,
    PartnerLinks,
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
            query=select(Links)
            .where(
                Links.id.in_(link_ids),
            )
            .options(
                selectinload(Links.offers),
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
            link_ids=link_ids,
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

    async def fetch_one(
        self,
        id: int,
        params: Params,
        session: AsyncSession | None = None,
    ) -> Optional[Partners]:
        return await self._fetch_one(
            query=select(self._table).where(
                self._table.id == id,
            ),
            pagination_query=(
                select(Links)
                .join(
                    PartnerLinks,
                    PartnerLinks.link_id == Links.id,
                )
                .where(
                    PartnerLinks.partner_id == id,
                )
                .options(
                    selectinload(Links.offers),
                )
            ),
            id=id,
            with_pagination=True,
            params=params,
            session=session,
        )

    async def fetch_many(
        self,
        session: AsyncSession | None = None,
    ) -> type[Partners] | None:
        return await self._fetch_many(
            query=select(
                self._table,
            ).order_by(desc(self._table.is_selected)),
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
