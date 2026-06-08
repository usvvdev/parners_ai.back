# application dependencies

from ..dto import (
    FetchOfferPosition,
    InsertOfferPosition,
    FiltersOfferPosition,
)

from libs.infrastructure.stores.clickhouse.repositories import OfferPositionRepository


class OfferPositionRepositoryView:
    def __init__(
        self,
        repository: OfferPositionRepository,
    ) -> None:
        self._repository = repository

    async def fetch(
        self,
        filters: FiltersOfferPosition,
    ) -> list[FetchOfferPosition]:
        return await self._repository.fetch_many(
            filters=filters,
        )

    async def insert(
        self,
        data: InsertOfferPosition,
    ) -> InsertOfferPosition:
        return await self._repository.insert(
            data=data,
        )
