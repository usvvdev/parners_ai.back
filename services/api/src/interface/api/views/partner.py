# application dependencies

from ..dto import (
    FetchPartner,
    FetchOffer,
    InsertPartner,
    FetchPartnerLinks,
)

from ...services import PartnerRepositoryService


class PartnerRepositoryView:
    def __init__(
        self,
        service: PartnerRepositoryService,
    ) -> None:
        self._service = service

    async def fetch(
        self,
    ) -> list[FetchPartner]:
        return await self._service.fetch()

    async def fetch_by_id(
        self,
        id: int,
    ) -> FetchPartnerLinks:
        return await self._service.fetch_by_id(
            id=id,
        )

    async def insert(
        self,
        data: InsertPartner,
    ) -> FetchPartner:
        return await self._service.insert(
            data=data.dump,
        )

    # async def update(
    #     self,
    #     offer_id: int,
    #     data: InsertOffer,
    # ) -> FetchOffer:
    #     return await self._service.update(
    #         offer_id=offer_id,
    #         data=data.dump,
    #     )

    async def delete(
        self,
        id: int,
    ) -> FetchOffer:
        return await self._service.delete(
            id=id,
        )
