# application dependencies

from .base import BaseAPIClient

from .pagination import (
    DEFAULT_PAGE_SIZE,
    parse_paginated_response,
)

from ....domain.types import Partner, PartnerDetail, PaginatedResponse


class PartnerAPIClient(BaseAPIClient):
    async def fetch_page(
        self,
        *,
        page: int = 1,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> PaginatedResponse[Partner]:
        data = await self._get(
            "/partners",
            params={"page": page, "size": size},
        )

        return parse_paginated_response(data, Partner)

    async def fetch_all(
        self,
        *,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> list[Partner]:
        items: list[Partner] = []
        page = 1

        while True:
            result = await self.fetch_page(page=page, size=size)
            items.extend(result.items)

            if page >= result.pages:
                break

            page += 1

        return items

    async def fetch_by_id(self, id: int) -> PartnerDetail:
        data = await self._get(f"/partners/{id}")

        return PartnerDetail.model_validate(data)

    async def create(
        self,
        payload: dict,
    ) -> PartnerDetail:
        data = await self._post(
            "/partners",
            json=payload,
        )

        return PartnerDetail.model_validate(data)

    async def update(
        self,
        id: int,
        payload: dict,
    ) -> PartnerDetail:
        data = await self._patch(
            f"/partners/{id}",
            json=payload,
        )

        return PartnerDetail.model_validate(data)

    async def delete(
        self,
        id: int,
    ) -> None:
        await self._delete(f"/partners/{id}")
