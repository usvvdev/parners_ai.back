# packages

from typing import (
    Any,
    Optional,
)

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
    ) -> Optional[Partners]:
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

    async def insert(
        self,
        data: dict[str, Any],
    ) -> Partners:
        async with self._engine.session_factory() as session:
            partner = Partners(
                title=data.get("title"),
                is_tracking=data.get("is_tracking", True),
            )

            if data.get("link_ids"):
                result = await session.execute(
                    select(Links).where(
                        Links.id.in_(data.get("link_ids")),
                    )
                )

                partner.links = result.scalars().all()

            session.add(partner)

            await session.commit()
            await session.refresh(partner)

            return partner
