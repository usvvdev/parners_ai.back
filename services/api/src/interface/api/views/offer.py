# application dependencies

from ..dto import (
    InsertOffer,
    FetchOffer,
    FetchOffers,
)

from ...services import OfferRepositoryService


class OfferRepositoryView:
    def __init__(
        self,
        service: OfferRepositoryService,
    ) -> None:
        self._service = service

    async def fetch(
        self,
    ) -> list[FetchOffers]:
        return await self._service.fetch()

    async def fetch_by_id(
        self,
        id: int,
    ) -> FetchOffer:
        return await self._service.fetch_by_id(
            id=id,
        )

    async def insert(
        self,
        data: InsertOffer,
    ) -> FetchOffer:
        return await self._service.insert(
            data=data,
        )

    async def update(
        self,
        id: int,
        data: InsertOffer,
    ) -> FetchOffer:
        return await self._service.update(
            id=id,
            data=data,
        )

    async def delete(
        self,
        id: int,
    ) -> FetchOffer:
        return await self._service.delete(
            id=id,
        )
