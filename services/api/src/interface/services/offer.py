# application dependencies

from typing import Any

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

    async def fetch_by_id(
        self,
        id: int,
    ) -> Offers:
        return await self._repository.fetch_by_id(
            id=id,
        )

    async def insert(
        self,
        data: Any,
    ) -> Offers:
        return await self._repository.insert(
            data=data,
        )

    async def update(
        self,
        id: int,
        data: Any,
    ) -> Offers:
        return await self._repository.update(
            id=id,
            data=data,
        )

    async def delete(
        self,
        id: int,
    ) -> Offers:
        return await self._repository.delete(
            id=id,
        )
