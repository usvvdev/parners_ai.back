# application dependencies

from typing import Any

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
    ) -> Partners:
        return await self._repository.fetch_by_id(
            id=id,
        )

    async def insert(
        self,
        data: dict[str, Any],
    ) -> Partners:
        return await self._repository.insert(
            data=data,
        )

    async def update(
        self,
        id: int,
        data: dict[str, Any],
    ) -> Partners:
        return await self._repository.update(
            id=id,
            data=data,
        )

    async def delete(
        self,
        id: int,
    ) -> Partners:
        return await self._repository.delete(
            id=id,
        )
