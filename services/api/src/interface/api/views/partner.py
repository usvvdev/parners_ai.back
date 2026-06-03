# application dependencies

from ..dto import FetchPartner, FetchOffer

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
    ) -> FetchPartner | None:
        return await self._service.fetch_by_id(
            id=id,
        )

    # async def create(
    #     self,
    #     data: InsertOffer,
    # ) -> FetchOffer:
    #     return await self._service.create(
    #         data=data.dump,
    #     )

    # async def update(
    #     self,
    #     offer_id: int,
    #     data: InsertOffer,
    # ) -> FetchOffer:
    #     return await self._service.update(
    #         offer_id=offer_id,
    #         data=data.dump,
    #     )

    # async def delete(
    #     self,
    #     offer_id: int,
    # ) -> FetchOffer:
    #     return await self._service.delete(
    #         offer_id=offer_id,
    #     )
