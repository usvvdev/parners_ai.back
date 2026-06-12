from typing import Any

from httpx import AsyncClient


class BaseAPIClient:
    def __init__(
        self,
        *,
        base_url: str,
    ) -> None:
        self._client = AsyncClient(
            base_url=base_url,
            timeout=60,
        )

    async def fetch(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        response = await self._client.get(
            endpoint,
            params=params,
        )

        response.raise_for_status()

        return response.json()

    async def post(
        self,
        endpoint: str,
        json: dict[str, Any],
    ) -> dict[str, Any]:
        response = await self._client.post(
            endpoint,
            json=json,
        )

        response.raise_for_status()

        return response.json()

    async def close(self) -> None:
        await self._client.aclose()
