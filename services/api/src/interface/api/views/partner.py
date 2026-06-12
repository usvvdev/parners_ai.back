# packages

from fastapi_pagination import Params

# application dependencies

from ..dto import (
    FetchPartner,
    FetchPartners,
    InsertPartner,
    UpdatePartner,
)

from libs.infrastructure.stores.mysql.repositories import PartnerRepository


class PartnerRepositoryView:
    def __init__(
        self,
        repository: PartnerRepository,
    ) -> None:
        self._repository = repository

    async def fetch(
        self,
    ) -> list[FetchPartner]:
        return await self._repository.fetch_many()

    async def fetch_by_id(
        self,
        id: int,
        params: Params,
    ) -> FetchPartners:
        partner, links = await self._repository.fetch_one(
            id=id,
            params=params,
        )
        return FetchPartners(
            **partner.__dict__,
            links=links,
        )

    async def insert(
        self,
        data: InsertPartner,
    ) -> FetchPartners:
        partner, links = await self._repository.insert(
            data=data,
        )
        return FetchPartners(
            **partner.__dict__,
            links=links,
        )

    async def update(
        self,
        id: int,
        data: UpdatePartner,
    ) -> FetchPartners:
        partner, links = await self._repository.update(
            id=id,
            data=data,
        )
        return FetchPartners(
            **partner.__dict__,
            links=links,
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        return await self._repository.delete(
            id=id,
        )
