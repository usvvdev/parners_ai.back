# application dependencies

from typing import Any

from libs.infrastructure.stores.mysql.models import Links

from libs.infrastructure.stores.mysql.repositories import LinkRepository


class LinkRepositoryService:
    def __init__(
        self,
        repository: LinkRepository,
    ) -> None:
        self._repository = repository

    async def fetch(
        self,
    ) -> list[Links]:
        return await self._repository.fetch()

    async def fetch_by_id(
        self,
        id: int,
    ) -> Links:
        return await self._repository.fetch_by_id(
            id=id,
        )

    async def insert(
        self,
        data: Any,
    ) -> Links:
        return await self._repository.insert(
            data=data,
        )

    async def update(
        self,
        id: int,
        data: Any,
    ) -> Links:
        return await self._repository.update(
            id=id,
            data=data,
        )

    async def delete(
        self,
        id: int,
    ) -> Links:
        return await self._repository.delete(
            id=id,
        )
