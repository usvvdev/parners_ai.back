from typing import Any

from ..base import BaseAPIClient


class OfferPositionAPIService:
    def __init__(
        self,
        api_client: BaseAPIClient,
    ) -> None:
        self._api_client = api_client

    async def create(
        self,
    ) -> list[Any]:
        data = await self._api_client.create(
            "/offer-positions",
        )
        return [LinkDTO.model_validate(item) for item in data]
