# application dependencies

from ..dto import (
    FetchUTMSource,
    FetchUTMSources,
    InsertUTMSource,
    UpdateUTMSource,
)

from libs.infrastructure.stores.mysql.repositories import UTMSourceRepository


class UTMSourceRepositoryView:
    def __init__(
        self,
        repository: UTMSourceRepository,
    ) -> None:
        self._repository = repository

    async def fetch(
        self,
    ) -> list[FetchUTMSources]:
        return await self._repository.fetch_many()

    async def fetch_by_id(
        self,
        id: int,
    ) -> FetchUTMSource:
        return await self._repository.fetch_one(
            id=id,
        )

    async def insert(
        self,
        data: InsertUTMSource,
    ) -> FetchUTMSource:
        return await self._repository.insert(
            data=data,
        )

    async def update(
        self,
        id: int,
        data: UpdateUTMSource,
    ) -> FetchUTMSource:
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
