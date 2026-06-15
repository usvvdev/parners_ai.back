from .resource import BaseResourceAPIClient

from ....domain.types._types import (
    FetchPartner,
    FetchPartners,
)


class PartnerAPIClient(
    BaseResourceAPIClient[FetchPartner, FetchPartners],
):
    path = "/partners"
    list_schema = FetchPartner
    detail_schema = FetchPartners
