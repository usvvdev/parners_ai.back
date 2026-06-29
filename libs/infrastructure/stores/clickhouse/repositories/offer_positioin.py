# packages

from typing import Any

from datetime import datetime

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_filters.ext.sqlalchemy import apply_filters

# application dependencies

from ..models import OfferPositions

from ..repository import ClickHouseRepository


class OfferPositionRepository(ClickHouseRepository[OfferPositions]):
    _table: type[OfferPositions] = OfferPositions

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

    async def fetch_many(
        self,
        filters: Any,
        session: AsyncSession | None = None,
    ) -> type[OfferPositions] | None:
        query = apply_filters(
            select(self._table),
            filters,
        )
        return await self._fetch_many(
            query=query,
            session=session,
        )

    async def _before_commit(
        self,
        entity: OfferPositions,
        data: Any,
        session: AsyncSession,
    ) -> None:
        if entity.created_at is None:
            entity.created_at = datetime.now()

    async def insert(
        self,
        data: Any,
        session: AsyncSession | None = None,
    ) -> type[OfferPositions]:
        return await self._insert(
            data=data,
            session=session,
        )
