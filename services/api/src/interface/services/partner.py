# application dependencies

from libs.infrastructure.stores.mysql.models import Partners

from libs.infrastructure.stores.mysql.repositories import PartnerRepository


class PartnerRepositoryService:
    def __init__(
        self,
        repository: PartnerRepository,
    ) -> None:
        self._repository = repository

    async def fetch(
        self,
    ) -> list[Partners]:
        return await self._repository.fetch()

    async def fetch_by_id(
        self,
        id: int,
    ) -> Partners | None:
        return await self._repository.fetch_by_id(
            id=id,
        )

    # async def update(
    #     self,
    #     offer_id: int,
    #     data: dict,
    # ) -> Partners:
    #     return await self._repository.update(
    #         id=offer_id,
    #         data=data,
    #     )

    # async def delete(
    #     self,
    #     offer_id: int,
    # ) -> Partners:
    #     return await self._repository.delete(
    #         id=offer_id,
    #     )
