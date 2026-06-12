# packages

from fastapi_pagination import Params

# application dependencies

from ..dto import (
    InsertLink,
    FetchLink,
    FetchLinks,
    UpdateLink,
)

from ....infrastructure.utils.functions import set_custom_pagination

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

    async def _to_fetch_link(
        self,
        id: int,
        params: Params | None = None,
    ) -> FetchLink:
        link, offers = await self._repository.fetch_one(
            id=id,
            params=params or set_custom_pagination(),
        )
        return FetchLink(
            **link.__dict__,
            offers=offers,
        )

    async def fetch_by_id(
        self,
        id: int,
        params: Params,
    ) -> FetchLink:
        return await self._to_fetch_link(
            id=id,
            params=params,
        )

    async def insert(
        self,
        data: InsertLink,
    ) -> FetchLink:
        link = await self._repository.insert(
            data=data,
        )
        return await self._to_fetch_link(
            id=link.id,
        )

    async def update(
        self,
        id: int,
        data: UpdateLink,
    ) -> FetchLink:
        await self._repository.update(
            id=id,
            data=data,
        )
        return await self._to_fetch_link(
            id=id,
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        return await self._repository.delete(
            id=id,
        )
