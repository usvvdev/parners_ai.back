# application depencies

from .base import BaseResourceAPIClient

from ....domain.types._types import (
    FetchLinks,
    FetchLink,
)


class LinkAPIClient(
    BaseResourceAPIClient[FetchLinks, FetchLink],
):
    path = "/links"
    list_schema = FetchLinks
    detail_schema = FetchLink
