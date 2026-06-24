# application dependencies

from ..schemas.offer_position import InsertOfferPosition

from ..resource import BaseResourceAPIClient


class OfferPositionAPIClient(BaseResourceAPIClient):
    path = "/offer-positions"

    detail_schema = InsertOfferPosition

    async def create(
        self,
        data: InsertOfferPosition,
    ) -> None:
        return await super().create(
            data=data,
        )
