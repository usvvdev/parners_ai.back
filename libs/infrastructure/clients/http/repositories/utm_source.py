# application dependencies

from ..schemas.utm_source import (
    FetchUTMSource,
    FetchUTMSources,
    InsertUTMSource,
)

from ..resource import BaseResourceAPIClient


class UTMSourceAPIClient(
    BaseResourceAPIClient[
        FetchUTMSources,
        FetchUTMSource,
    ],
):
    path = "/utm-sources"

    list_schema = FetchUTMSources
    detail_schema = FetchUTMSource

    detail_paginated = False

    async def create(
        self,
        data: InsertUTMSource,
    ) -> FetchUTMSource:
        return await self.create(
            data,
        )
