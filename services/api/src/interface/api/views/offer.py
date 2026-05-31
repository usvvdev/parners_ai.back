# application dependencies

from ..dto import (
    InsertOffer,
    FetchOffer,
)

from ...services.offer import OfferRepositoryService


class OfferRepositoryView:
    def __init__(
        self,
        service: OfferRepositoryService,
    ) -> None:
        self._service = service

    async def fetch(
        self,
    ) -> list[FetchOffer]:
        data = await self._service.fetch()
        return [FetchOffer.model_validate(item) for item in data]

    async def create(
        self,
        data: InsertOffer,
    ) -> FetchOffer:
        return await self._service.create(
            data=data.dump,
        )

    async def update(
        self,
        offer_id: int,
        data: InsertOffer,
    ) -> FetchOffer:
        return await self._service.update(
            offer_id=offer_id,
            data=data.dump,
        )

    async def delete(
        self,
        offer_id: int,
    ) -> FetchOffer:
        return await self._service.delete(
            offer_id=offer_id,
        )
