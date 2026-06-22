# application dependencies

from ..schemas.offer import (
    FetchOffer,
    FetchOffers,
)

from ..resource import BaseResourceAPIClient


class OfferAPIClient(
    BaseResourceAPIClient[
        FetchOffers,
        FetchOffer,
    ],
):
    path = "/offers"

    list_schema = FetchOffers
    detail_schema = FetchOffer

    detail_paginated = False
