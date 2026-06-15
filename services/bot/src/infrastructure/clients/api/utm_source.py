# application depencies

from .base import BaseResourceAPIClient

from ....domain.types._types import FetchUTMSource


class UTMSourceAPIClient(
    BaseResourceAPIClient[FetchUTMSource, FetchUTMSource],
):
    path = "/utm-sources"
    list_schema = FetchUTMSource
    detail_schema = FetchUTMSource
    detail_paginated = False
