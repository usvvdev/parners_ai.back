# application dependencies

from .base import BaseAPIClient

from .pagination import (
    DEFAULT_PAGE_SIZE,
    parse_paginated_response,
)

from ....domain.types import LinkSummary, LinkDetail, PaginatedResponse


class LinkAPIClient(BaseAPIClient):
    async def fetch_page(
        self,
        *,
        page: int = 1,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> PaginatedResponse[LinkSummary]:
        data = await self._get(
            "/links",
            params={"page": page, "size": size},
        )

        return parse_paginated_response(data, LinkSummary)

    async def fetch_all(
        self,
        *,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> list[LinkSummary]:
        items: list[LinkSummary] = []
        page = 1

        while True:
            result = await self.fetch_page(page=page, size=size)
            items.extend(result.items)

            if page >= result.pages:
                break

            page += 1

        return items

    async def fetch_by_id(self, id: int) -> LinkDetail:
        data = await self._get(f"/links/{id}")

        return LinkDetail.model_validate(data)

    async def create(
        self,
        payload: dict,
    ) -> LinkDetail:
        data = await self._post(
            "/links",
            json=payload,
        )

        return LinkDetail.model_validate(data)

    async def update(
        self,
        id: int,
        payload: dict,
    ) -> LinkDetail:
        data = await self._patch(
            f"/links/{id}",
            json=payload,
        )

        return LinkDetail.model_validate(data)

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._delete(f"/links/{id}")
