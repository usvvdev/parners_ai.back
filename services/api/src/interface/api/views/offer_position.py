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
        entities = await self._repository.fetch_many(
            filters=filters,
        )

        return [
            FetchOfferPosition.model_validate(
                entity,
                from_attributes=True,
            )
            for entity in entities
        ]

    async def insert(
        self,
        data: InsertOfferPosition,
    ) -> FetchOfferPosition:
        entity = await self._repository.insert(
            data=data,
        )

        return FetchOfferPosition.model_validate(
            entity,
            from_attributes=True,
        )
