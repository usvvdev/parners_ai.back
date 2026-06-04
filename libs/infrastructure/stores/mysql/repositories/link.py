# packages

from typing import (
    Any,
    Optional,
)

from sqlalchemy import select

from sqlalchemy.orm import selectinload

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

            if offer_ids:
                query = (
                    select(Offers).where(
                        Offers.id.in_(offer_ids),
                    ),
                )

                link.offers = await super().fetch(
                    query=query,
                    session=session,
                )

            session.add(link)

            await session.commit() and await session.refresh(
                link,
            )

            return link

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
                [],
            )

            query = (
                select(self._table)
                .options(
                    selectinload(self._table.offers),
                )
                .where(
                    self._table.id == id,
                )
            )

            link = await super().fetch(
                query=query,
                many=False,
                session=session,
                id=id,
            )

            for field, value in payload.items():
                setattr(
                    link,
                    field,
                    value,
                )

            if offer_ids is not None:
                query = select(Offers).where(
                    Offers.id.in_(offer_ids),
                )

                link.offers = (
                    await super().fetch(
                        query=query,
                        session=session,
                    )
                    if offer_ids
                    else []
                )

            await session.commit() and await session.refresh(link)

            return link
