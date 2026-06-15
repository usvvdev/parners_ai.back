# packages

from typing import (
    Any,
)

from sqlalchemy import (
    delete,
    select,
    desc,
)

from fastapi_pagination import Params

from sqlalchemy.orm import selectinload

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_filters.ext.sqlalchemy import apply_filters

# application dependencies

from ..models import (
    Partners,
    Links,
    UtmSources,
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

    async def __sync_links(
        self,
        session: AsyncSession,
        partner_id: int,
        link_ids: list[int],
    ) -> None:
        await session.execute(
            delete(PartnerLinks).where(PartnerLinks.partner_id == partner_id),
        )

        if link_ids:
            session.add_all(
                [
                    PartnerLinks(
                        partner_id=partner_id,
                        link_id=link_id,
                    )
                    for link_id in link_ids
                ],
            )

    async def __commit_links(
        self,
        entity: Partners,
        session: AsyncSession,
        link_ids: list[int] | None,
    ) -> None:
        if link_ids is None:
            return

        if entity.id:
            await self.__sync_links(
                session,
                entity.id,
                link_ids,
            )
            return

        entity.links = await self.__fetch_links(
            session=session,
            link_ids=link_ids,
        )

    async def _before_commit(
        self,
        entity: Partners,
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
        params: Params | None = None,
        session: AsyncSession | None = None,
    ) -> tuple[Partners, Any] | Partners:
        pagination = self._list_params(params)

        return await self._fetch_one(
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
            with_pagination=self._paginate_on_read(session),
            params=pagination,
            session=session,
        )

    async def fetch_many(
        self,
        filters: Any,
        session: AsyncSession | None = None,
    ) -> type[Partners] | None:
        query = (
            select(self._table)
            .options(
                selectinload(self._table.utm_source),
            )
            .order_by(desc(self._table.is_selected))
            .join(UtmSources)
        )
        return await self._fetch_many(
            query=apply_filters(
                query,
                filters=filters,
            ),
            session=session,
        )

    async def insert(
        self,
        data: Any,
        *,
        session: AsyncSession | None = None,
    ) -> tuple[Partners, Any]:
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
    ) -> tuple[Partners, Any]:
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
