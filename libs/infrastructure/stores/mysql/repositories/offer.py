# packages

from typing import (
    Any,
    Optional,
)

from sqlalchemy import select

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

    async def fetch_by_id(
        self,
        id: int,
    ) -> Optional[Offers]:
        query = select(self._table).where(self._table.id == id)
        return await super().fetch(
            query=query,
            many=False,
            id=id,
        )

    async def insert(
        self,
        data: Any,
    ) -> Offers:
        async with self._engine.session_factory() as session:
            payload = data.model_dump(
                exclude_unset=True,
            )

            offer = self._table(
                **payload,
            )

            session.add(offer)

            await session.commit() and await session.refresh(
                offer,
            )

            return offer

    async def update(
        self,
        id: int,
        data: Any,
    ) -> Offers:
        async with self._engine.session_factory() as session:
            payload = data.model_dump(
                exclude_unset=True,
            )

            query = select(self._table).where(
                self._table.id == id,
            )

            offer = await super().fetch(
                query=query,
                many=False,
                session=session,
                id=id,
            )

            for field, value in payload.items():
                setattr(
                    offer,
                    field,
                    value,
                )

                await session.commit() and await session.refresh(offer)

            return offer
