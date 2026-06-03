# packages

from typing import Optional

from sqlalchemy import select

from sqlalchemy.orm import selectinload

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

    async def fetch_by_id(
        self,
        id: int,
    ):
        query = (
            select(self._table)
            .options(
                selectinload(self._table.links).selectinload(Links.offers),
            )
            .where(self._table.id == id)
        )
        return await super().fetch(
            query=query,
            many=False,
            id=id,
        )
