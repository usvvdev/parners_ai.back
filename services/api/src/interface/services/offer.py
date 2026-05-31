# application dependencies

from libs.infrastructure.stores.mysql.models import Offers

from libs.infrastructure.stores.mysql.repositories import OfferRepository


class OfferRepositoryService:
    def __init__(
        self,
        repository: OfferRepository,
    ) -> None:
        self._repository = repository

    async def fetch(
        self,
    ) -> list[Offers]:
        return await self._repository.fetch()

    async def create(
        self,
        data: dict,
    ) -> Offers:
        return await self._repository.insert(
            data=data,
        )

    async def delete(
        self,
        offer_id: int,
    ) -> Offers:
        return await self._repository.delete(
            id=offer_id,
        )
