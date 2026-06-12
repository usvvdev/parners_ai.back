# packages

from fastapi_pagination import Params

# application dependencies

from ..dto import (
    FetchPartner,
    FetchPartners,
    InsertPartner,
    UpdatePartner,
)

from ....infrastructure.utils.functions import set_custom_pagination

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

    async def _to_fetch_partners(
        self,
        id: int,
        params: Params | None = None,
    ) -> FetchPartners:
        partner, links = await self._repository.fetch_one(
            id=id,
            params=params or set_custom_pagination(),
        )
        return FetchPartners(
            **partner.__dict__,
            links=links,
        )

    async def fetch_by_id(
        self,
        id: int,
        params: Params,
    ) -> FetchPartners:
        return await self._to_fetch_partners(
            id=id,
            params=params,
        )

    async def insert(
        self,
        data: InsertPartner,
    ) -> FetchPartners:
        partner = await self._repository.insert(
            data=data,
        )
        return await self._to_fetch_partners(
            id=partner.id,
        )

    async def update(
        self,
        id: int,
        data: UpdatePartner,
    ) -> FetchPartners:
        await self._repository.update(
            id=id,
            data=data,
        )
        return await self._to_fetch_partners(
            id=id,
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        return await self._repository.delete(
            id=id,
        )
