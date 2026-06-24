# application dependencies

from ..schemas.partner import (
    FetchPartner,
    FetchPartners,
)

from ..resource import BaseResourceAPIClient


class PartnerAPIClient(
    BaseResourceAPIClient[
        FetchPartner,
        FetchPartners,
    ],
):
    path = "/partners"

    list_schema = FetchPartners
    detail_schema = FetchPartner
