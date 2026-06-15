# packages

from typing import (
    Any,
)

from sqlalchemy import (
    delete,
    select,
)

from sqlalchemy.orm import selectinload

from fastapi_pagination import Params

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_filters.ext.sqlalchemy import apply_filters

# application dependencies

from ..models import (
    Links,
    Offers,
    LinkOffers,
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

    async def __sync_offers(
        self,
        session: AsyncSession,
        link_id: int,
        offer_ids: list[int],
    ) -> None:
        await session.execute(
            delete(LinkOffers).where(LinkOffers.link_id == link_id),
        )

        if offer_ids:
            session.add_all(
                [
                    LinkOffers(
                        link_id=link_id,
                        offer_id=offer_id,
                    )
                    for offer_id in offer_ids
                ],
            )

    async def __commit_offers(
        self,
        entity: Links,
        session: AsyncSession,
        offer_ids: list[int] | None,
    ) -> None:
        if offer_ids is None:
            return

        if entity.id:
            await self.__sync_offers(
                session,
                entity.id,
                offer_ids,
            )
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

    async def fetch_one(
        self,
        id: int,
        params: Params | None = None,
        session: AsyncSession | None = None,
    ) -> tuple[Links, Any] | Links:
        pagination = self._list_params(params)

        return await self._fetch_one(
            pagination_query=(
                select(Offers)
                .join(
                    LinkOffers,
                    LinkOffers.offer_id == Offers.id,
                )
                .where(
                    LinkOffers.link_id == id,
                )
            ),
            id=id,
            with_pagination=self._paginate_on_read(session),
            params=pagination,
            session=session,
        )

    async def fetch_many(
        self,
        filters: Any,
        session: AsyncSession | None = None,
    ) -> type[Links] | None:
        query = apply_filters(
            select(
                self._table,
            ).options(
                selectinload(self._table.offers),
            ),
            filters=filters,
        )
        return await self._fetch_many(
            query=query,
            session=session,
        )

    async def insert(
        self,
        data: Any,
        *,
        session: AsyncSession | None = None,
    ) -> tuple[Links, Any]:
        entity = await self._insert(
            data,
            session=session,
        )

        return await self.fetch_one(
            id=entity.id,
        )

    async def update(
        self,
        id: int,
        data: Any,
        *,
        session: AsyncSession | None = None,
    ) -> tuple[Links, Any]:
        await self._update(
            id=id,
            data=data,
            session=session,
        )

        return await self.fetch_one(
            id=id,
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
