# application dependencies

from .base import BaseAPIClient

from .pagination import (
    DEFAULT_PAGE_SIZE,
    parse_paginated_response,
)

from ....domain.types import OfferSummary, PaginatedResponse


class OfferAPIClient(BaseAPIClient):
    async def fetch_page(
        self,
        *,
        page: int = 1,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> PaginatedResponse[OfferSummary]:
        data = await self._get(
            "/offers",
            params={"page": page, "size": size},
        )

        return parse_paginated_response(data, OfferSummary)

    async def fetch_all(
        self,
        *,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> list[OfferSummary]:
        items: list[OfferSummary] = []
        page = 1

        while True:
            result = await self.fetch_page(page=page, size=size)
            items.extend(result.items)

            if page >= result.pages:
                break

            page += 1

        return items

    async def fetch_by_id(self, id: int) -> OfferSummary:
        data = await self._get(f"/offers/{id}")

        return OfferSummary.model_validate(data)

    async def create(
        self,
        payload: dict,
    ) -> OfferSummary:
        data = await self._post(
            "/offers",
            json=payload,
        )

        return OfferSummary.model_validate(data)

    async def update(
        self,
        id: int,
        payload: dict,
    ) -> OfferSummary:
        data = await self._patch(
            f"/offers/{id}",
            json=payload,
        )

        return OfferSummary.model_validate(data)

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._delete(f"/offers/{id}")
