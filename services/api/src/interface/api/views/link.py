# application dependencies

from ..dto import (
    InsertLink,
    FetchLink,
)

from ...services import LinkRepositoryService


class LinkRepositoryView:
    def __init__(
        self,
        service: LinkRepositoryService,
    ) -> None:
        self._service = service

    async def fetch(
        self,
    ) -> list[FetchLink]:
        return await self._service.fetch()

    async def fetch_by_id(
        self,
        id: int,
    ) -> FetchLink:
        return await self._service.fetch_by_id(
            id=id,
        )

    async def create(
        self,
        data: InsertLink,
    ) -> FetchLink:
        return await self._service.create(
            data=data,
        )

    async def update(
        self,
        id: int,
        data: InsertLink,
    ) -> FetchLink:
        return await self._service.update(
            id=id,
            data=data,
        )

    async def delete(
        self,
        id: int,
    ) -> FetchLink:
        return await self._service.delete(
            id=id,
        )
