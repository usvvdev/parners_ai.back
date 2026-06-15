from ....core.constants import DEFAULT_PAGE_SIZE
from .resource import BaseResourceAPIClient

from ....domain.types._types import FetchLinks


class LinkAPIClient(
    BaseResourceAPIClient[FetchLinks, FetchLinks],
):
    path = "/links"
    list_schema = FetchLinks
    detail_schema = FetchLinks
    detail_paginated = False

    async def fetch_all_active(
        self,
        *,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> list[FetchLinks]:
        return await self.fetch_all(
            size=size,
            filters={"is_active": True},
        )
