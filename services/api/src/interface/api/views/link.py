# packages

from fastapi_pagination import Params

# application dependencies

from ..dto import (
    InsertLink,
    FetchLink,
    FetchLinks,
    UpdateLink,
)

from libs.infrastructure.stores.mysql.repositories import LinkRepository


class LinkRepositoryView:
    def __init__(
        self,
        repository: LinkRepository,
    ) -> None:
        self._repository = repository

    async def fetch(
        self,
    ) -> list[FetchLinks]:
        return await self._repository.fetch_many()

    async def fetch_by_id(
        self,
        id: int,
        params: Params,
    ) -> FetchLink:
        link, offers = await self._repository.fetch_one(
            id=id,
            params=params,
        )
        return FetchLink(
            **link.__dict__,
            offers=offers,
        )

    async def insert(
        self,
        data: InsertLink,
    ) -> FetchLink:
        return await self._repository.insert(
            data=data,
        )

    async def update(
        self,
        id: int,
        data: UpdateLink,
    ) -> FetchLink:
        return await self._repository.update(
            id=id,
            data=data,
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        return await self._repository.delete(
            id=id,
        )
