# packages

from typing import Optional

from sqlalchemy import select

from sqlalchemy.orm import selectinload

# application dependencies

from ..models import Partners

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

    async def fetch(
        self,
        partner_id: Optional[int] = None,
    ):
        query = select(self._table).options(
            selectinload(self._table.offers),
            selectinload(self._table.links),
        )
        if partner_id:
            query = query.where(self._table.id == partner_id)

        return await super().fetch(
            query=query,
        )
