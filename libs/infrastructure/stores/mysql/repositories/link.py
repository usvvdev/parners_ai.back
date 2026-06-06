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
        offer_ids: list[int],
    ) -> list[Offers]:
        if not offer_ids:
            return []

        query = select(Offers).where(
            Offers.id.in_(offer_ids),
        )

        return await super().fetch(
            query=query,
            session=session,
        )

    async def __commit_offers(
        self,
        obj: Links,
        session: AsyncSession,
        offer_ids: list[int] | None,
    ) -> None:
        if offer_ids is None:
            return

        obj.offers = await self.__fetch_offers(
            session=session,
            offer_ids=offer_ids,
        )

    async def __fetch_relations(
        self,
        session: AsyncSession,
        obj_id: int,
    ) -> Links:
        query = (
            select(self._table)
            .options(
                selectinload(self._table.offers),
            )
            .where(
                self._table.id == obj_id,
            )
        )

        result = await session.execute(query)

        return result.scalar_one()

    async def fetch_by_id(
        self,
        id: int,
    ) -> Optional[Links]:
        query = (
            select(self._table)
            .options(
                selectinload(self._table.offers),
            )
            .where(self._table.id == id)
        )
        return await super().fetch(
            query=query,
            many=False,
            id=id,
        )

    async def insert(
        self,
        data: Any,
    ) -> Links:
        async with self._engine.session_factory() as session:
            payload = data.model_dump(
                exclude_unset=True,
            )

            offer_ids = payload.pop(
                "offer_ids",
                [],
            )

            link = self._table(
                **payload,
            )

            await self.__commit_offers(
                obj=link,
                session=session,
                offer_ids=offer_ids,
            )

            session.add(link)

            await session.commit() and await session.refresh(link)

            return await self.__fetch_relations(
                session=session,
                obj_id=link.id,
            )

    async def update(
        self,
        id: int,
        data: Any,
    ) -> Links:
        async with self._engine.session_factory() as session:
            payload = data.model_dump(
                exclude_unset=True,
            )

            offer_ids = payload.pop(
                "offer_ids",
                None,
            )

            link = await self.__fetch_relations(
                session=session,
                obj_id=id,
            )

            for field, value in payload.items():
                setattr(
                    link,
                    field,
                    value,
                )

            if offer_ids is not None:
                link.offers = await self.__fetch_offers(
                    session=session,
                    offer_ids=offer_ids,
                )

            await session.commit()

            return await self.__fetch_relations(
                session=session,
                obj_id=id,
            )
