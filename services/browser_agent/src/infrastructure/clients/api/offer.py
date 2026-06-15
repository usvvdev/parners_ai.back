from .resource import BaseResourceAPIClient

from ....domain.types._types import FetchOffer


class OfferAPIClient(
    BaseResourceAPIClient[FetchOffer, FetchOffer],
):
    path = "/offers"
    list_schema = FetchOffer
    detail_schema = FetchOffer
    detail_paginated = False
