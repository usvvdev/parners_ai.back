from typing import Any

from ..base import BaseAPIClient


class PartnerAPIService:
    def __init__(
        self,
        api_client: BaseAPIClient,
    ) -> None:
        self._api_client = api_client

    async def create(
        self,
        data: PartnerResult,
    ) -> list[Any]:
        data = await self._api_client.post(
            "/partners",
            json=data,
        )
        return data
