# application depencies

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
    ) -> PaginatedResponse[FetchLinks]:
        return await self._link_client.fetch_page(page=page)

    async def fetch_by_id(
        self,
        id: int,
    ) -> FetchLink:
        return await self._link_client.fetch_by_id(id)

    async def toggle(
        self,
        id: int,
    ) -> tuple[FetchLink, bool]:
        link = await self._link_client.fetch_by_id(id)
        new_status = not link.is_active

        await self._link_client.update(
            id,
            UpdateLink(is_active=new_status),
        )

        return await self._link_client.fetch_by_id(id), new_status

    async def update_url(
        self,
        id: int,
        url: str,
    ) -> FetchLink:
        await self._link_client.update(
            id,
            UpdateLink(link=url),
        )

        return await self._link_client.fetch_by_id(id)

    async def create_with_offers(
        self,
        data: InsertLink,
        *,
        p_id: int = 0,
    ) -> FetchLink | FetchPartners:
        created = await self._link_client.create(data)

        if p_id:
            partner = await self._partner_client.fetch_by_id(p_id)
            link_ids = [item.id for item in partner.links]

            return await self._partner_client.update(
                p_id,
                UpdatePartner(link_ids=[*link_ids, created.id]),
            )

        return created

    async def update_offers(
        self,
        id: int,
        offer_ids: list[int],
    ) -> FetchLink:
        await self._link_client.update(
            id,
            UpdateLink(offer_ids=offer_ids),
        )

        return await self._link_client.fetch_by_id(id)

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._link_client.delete(id)

    async def fetch_offer_ids(
        self,
        id: int,
    ) -> list[int]:
        link = await self._link_client.fetch_by_id(id)

        return [offer.id for offer in link.offers]

    async def fetch_all_offers(self) -> list[FetchOffer]:
        return await self._offer_client.fetch_all()
