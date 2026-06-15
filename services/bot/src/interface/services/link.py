# application depencies

from ...core.constants import FILTER_ALL

from ...infrastructure.clients.api import (
    LinkAPIClient,
    PartnerAPIClient,
    OfferAPIClient,
)

from ...domain.types._types import (
    FetchLink,
    FetchOffer,
    FetchPartners,
    InsertLink,
    UpdateLink,
    UpdatePartner,
    PaginatedResponse,
    FetchLinks,
)


class LinkService:
    def __init__(
        self,
        link_client: LinkAPIClient,
        partner_client: PartnerAPIClient,
        offer_client: OfferAPIClient,
    ) -> None:
        self._link_client = link_client
        self._partner_client = partner_client
        self._offer_client = offer_client

    async def fetch(
        self,
        *,
        page: int = 1,
        is_active: int = FILTER_ALL,
    ) -> PaginatedResponse[FetchLinks]:
        filters: dict[str, bool] = {}

        if is_active != FILTER_ALL:
            filters["is_active"] = bool(is_active)

        return await self._link_client.fetch_page(
            page=page,
            filters=filters or None,
        )

    async def fetch_by_id(
        self,
        id: int,
        *,
        page: int = 1,
    ) -> FetchLink:
        return await self._link_client.fetch_by_id(
            id,
            page=page,
        )

    async def toggle(
        self,
        id: int,
        *,
        page: int = 1,
    ) -> tuple[FetchLink, bool]:
        link = await self._link_client.fetch_by_id(
            id,
            page=page,
        )
        new_status = not link.is_active

        await self._link_client.update(
            id,
            UpdateLink(is_active=new_status),
        )

        return await self._link_client.fetch_by_id(
            id,
            page=page,
        ), new_status

    async def update_url(
        self,
        id: int,
        url: str,
        *,
        page: int = 1,
    ) -> FetchLink:
        await self._link_client.update(
            id,
            UpdateLink(link=url),
        )

        return await self._link_client.fetch_by_id(
            id,
            page=page,
        )

    async def create_with_offers(
        self,
        data: InsertLink,
        *,
        p_id: int = 0,
    ) -> FetchLink | FetchPartners:
        created = await self._link_client.create(data)

        if p_id:
            link_ids = await self._fetch_all_partner_link_ids(p_id)

            return await self._partner_client.update(
                p_id,
                UpdatePartner(link_ids=[*link_ids, created.id]),
            )

        return created

    async def update_offers(
        self,
        id: int,
        offer_ids: list[int],
        *,
        page: int = 1,
    ) -> FetchLink:
        await self._link_client.update(
            id,
            UpdateLink(offer_ids=offer_ids),
        )

        return await self._link_client.fetch_by_id(
            id,
            page=page,
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._link_client.delete(id)

    async def fetch_offer_ids(
        self,
        id: int,
    ) -> list[int]:
        offer_ids: list[int] = []
        page = 1

        while True:
            link = await self._link_client.fetch_by_id(
                id,
                page=page,
            )
            offer_ids.extend(offer.id for offer in link.offers.items)

            if page >= link.offers.pages:
                break

            page += 1

        return offer_ids

    async def fetch_offers(
        self,
        *,
        page: int = 1,
    ) -> PaginatedResponse[FetchOffer]:
        return await self._offer_client.fetch_page(page=page)

    async def _fetch_all_partner_link_ids(
        self,
        p_id: int,
    ) -> list[int]:
        link_ids: list[int] = []
        page = 1

        while True:
            partner = await self._partner_client.fetch_by_id(
                p_id,
                page=page,
            )
            link_ids.extend(link.id for link in partner.links.items)

            if page >= partner.links.pages:
                break

            page += 1

        return link_ids
