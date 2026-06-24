# application depencies

from libs.infrastructure.clients.http.repositories import (
    OfferAPIClient,
    LinkAPIClient,
)

from libs.infrastructure.clients.http.schemas import (
    FetchOffer,
    FetchLink,
    InsertOffer,
    UpdateOffer,
    UpdateLink,
)

from libs.domain.types._types.shared import PaginatedResponse


class OfferService:
    def __init__(
        self,
        offer_client: OfferAPIClient,
        link_client: LinkAPIClient,
    ) -> None:
        self._offer_client = offer_client
        self._link_client = link_client

    async def fetch(
        self,
        *,
        page: int = 1,
    ) -> PaginatedResponse[FetchOffer]:
        return await self._offer_client.fetch_page(page=page)

    async def fetch_by_id(
        self,
        id: int,
    ) -> FetchOffer:
        return await self._offer_client.fetch_by_id(id)

    async def create(
        self,
        data: InsertOffer,
        *,
        l_id: int = 0,
    ) -> FetchOffer | FetchLink:
        offer = await self._offer_client.create(data)

        if l_id:
            link = await self._link_client.fetch_by_id(l_id)
            offer_ids = [item.id for item in link.offers]

            await self._link_client.update(
                l_id,
                UpdateLink(offer_ids=[*offer_ids, offer.id]),
            )

            return await self._link_client.fetch_by_id(l_id)

        return offer

    async def update_title(
        self,
        id: int,
        title: str,
    ) -> FetchOffer:
        return await self._offer_client.update(
            id,
            UpdateOffer(title=title),
        )

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._offer_client.delete(id)

    async def fetch_link(
        self,
        id: int,
    ) -> FetchLink:
        return await self._link_client.fetch_by_id(id)
