from .resource import BaseResourceAPIClient

from ....domain.types._types import FetchLinks


class LinkAPIClient(
    BaseResourceAPIClient[FetchLinks, FetchLinks],
):
    path = "/links"
    list_schema = FetchLinks
    detail_schema = FetchLinks
    detail_paginated = False
