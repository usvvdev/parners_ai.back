from .base import BaseAPIClient

from ....domain.types._types import InsertOfferPosition


class OfferPositionAPIClient(BaseAPIClient):
    path = "/offer-positions"

    async def create(
        self,
        data: InsertOfferPosition,
    ) -> None:
        await self._post(
            self.path,
            json=data.model_dump(
                mode="json",
                exclude_none=True,
            ),
        )
