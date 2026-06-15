from .resource import BaseResourceAPIClient

from ....domain.types._types import (
    FetchUTMSource,
    InsertUTMSource,
)


class UTMSourceAPIClient(
    BaseResourceAPIClient[FetchUTMSource, FetchUTMSource],
):
    path = "/utm-sources"
    list_schema = FetchUTMSource
    detail_schema = FetchUTMSource
    detail_paginated = False

    async def create(
        self,
        data: InsertUTMSource,
    ) -> FetchUTMSource:
        return await super().create(data)
