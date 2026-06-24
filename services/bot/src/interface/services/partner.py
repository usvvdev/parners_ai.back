# application depencies

from ...core.constants import FILTER_ALL

from libs.infrastructure.clients.http.repositories import (
    PartnerAPIClient,
    LinkAPIClient,
    UTMSourceAPIClient,
)

from libs.infrastructure.clients.http.schemas import (
    FetchPartner,
    FetchPartners,
    FetchLinks,
    FetchUTMSource,
    InsertPartner,
    UpdatePartner,
)

from libs.domain.types._types.shared import PaginatedResponse


class PartnerService:
    def __init__(
        self,
        partner_client: PartnerAPIClient,
        link_client: LinkAPIClient,
        utm_source_client: UTMSourceAPIClient,
    ) -> None:
        self._partner_client = partner_client
        self._link_client = link_client
        self._utm_source_client = utm_source_client

    async def fetch(
        self,
        *,
        page: int = 1,
        is_tracking: int = FILTER_ALL,
        is_selected: int = FILTER_ALL,
    ) -> PaginatedResponse[FetchPartner]:
        filters: dict[str, bool] = {}

        if is_tracking != FILTER_ALL:
            filters["is_tracking"] = bool(is_tracking)

        if is_selected != FILTER_ALL:
            filters["is_selected"] = bool(is_selected)

        return await self._partner_client.fetch_page(
            page=page,
            filters=filters or None,
        )

    async def fetch_by_id(
        self,
        id: int,
        *,
        page: int = 1,
    ) -> FetchPartners:
        return await self._partner_client.fetch_by_id(
            id,
            page=page,
        )

    async def create(
        self,
        data: InsertPartner,
    ) -> PaginatedResponse[FetchPartner]:
        await self._partner_client.create(data)

        return await self.fetch(page=1)

    async def toggle_tracking(
        self,
        id: int,
        *,
        is_tracking: bool,
    ) -> FetchPartners:
        return await self._partner_client.update(
            id,
            UpdatePartner(is_tracking=not is_tracking),
        )

    async def toggle_selected(
        self,
        id: int,
        *,
        is_selected: bool,
    ) -> FetchPartners:
        return await self._partner_client.update(
            id,
            UpdatePartner(is_selected=not is_selected),
        )

    async def update_links(
        self,
        id: int,
        link_ids: list[int],
    ) -> FetchPartners:
        return await self._partner_client.update(
            id,
            UpdatePartner(link_ids=link_ids),
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._partner_client.delete(id)

    async def fetch_link_ids(
        self,
        id: int,
    ) -> list[int]:
        link_ids: list[int] = []
        page = 1

        while True:
            partner = await self._partner_client.fetch_by_id(
                id,
                page=page,
            )
            link_ids.extend(link.id for link in partner.links.items)

            if page >= partner.links.pages:
                break

            page += 1

        return link_ids

    async def fetch_links(
        self,
        *,
        page: int = 1,
    ) -> PaginatedResponse[FetchLinks]:
        return await self._link_client.fetch_page(page=page)

    async def fetch_utm_sources(
        self,
        *,
        page: int = 1,
    ) -> PaginatedResponse[FetchUTMSource]:
        return await self._utm_source_client.fetch_page(page=page)
