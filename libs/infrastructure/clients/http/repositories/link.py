# application dependencies

from ..schemas.link import (
    FetchLink,
    FetchLinks,
)

from ..resource import BaseResourceAPIClient

from libs.core.constants import DEFAULT_PAGE_SIZE


class LinkAPIClient(
    BaseResourceAPIClient[
        FetchLinks,
        FetchLink,
    ],
):
    path = "/links"

    list_schema = FetchLinks
    detail_schema = FetchLink

    async def fetch_all(
        self,
        *,
        size: int = DEFAULT_PAGE_SIZE,
    ) -> list[FetchLinks]:
        return await super().fetch_all(
            size=size,
            filters={
                "is_active": True,
            },
        )
