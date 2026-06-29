# application dependencies

from ..schemas.offer_position import (
    FetchOfferPosition,
    InsertOfferPosition,
)

from ..resource import BaseResourceAPIClient


class OfferPositionAPIClient(
    BaseResourceAPIClient[
        FetchOfferPosition,
        FetchOfferPosition,
    ],
):
    path = "/offer-positions"

    list_schema = FetchOfferPosition
    detail_schema = FetchOfferPosition

    async def create(
        self,
        data: InsertOfferPosition,
    ) -> FetchOfferPosition:
        return await super().create(
            data=data,
        )
