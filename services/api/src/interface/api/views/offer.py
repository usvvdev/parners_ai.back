# application dependencies

from ..dto import (
    FetchOffer,
    FetchOffers,
    InsertOffer,
    UpdateOffer,
)

from libs.infrastructure.stores.mysql.repositories import OfferRepository


class OfferRepositoryView:
    def __init__(
        self,
        repository: OfferRepository,
    ) -> None:
        self._repository = repository

    async def fetch(
        self,
    ) -> list[FetchOffers]:
        return await self._repository.fetch_many()

    async def fetch_by_id(
        self,
        id: int,
    ) -> FetchOffer:
        return await self._repository.fetch_one(
            id=id,
        )

    async def insert(
        self,
        data: InsertOffer,
    ) -> FetchOffer:
        return await self._repository.insert(
            data=data,
        )

    async def update(
        self,
        id: int,
        data: UpdateOffer,
    ) -> FetchOffer:
        return await self._repository.update(
            id=id,
            data=data,
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        return await self._repository.delete(
            id=id,
        )
