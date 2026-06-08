from typing import Any

from ..base import BaseAPIClient


class LinkApiService:
    def __init__(
        self,
        api_client: BaseAPIClient,
    ) -> None:
        self._api_client = api_client

    async def fetch_many(
        self,
    ) -> list[Any]:
        data = await self._api_client.fetch(
            "/links",
        )
        return [LinkDTO.model_validate(item) for item in data]
