from typing import Any

from httpx import AsyncClient


class BaseHTTPClient:
    def __init__(
        self,
        *,
        client: AsyncClient,
    ) -> None:
        self._client = client

    async def get(
        self,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self._client.get(
            endpoint,
            params=params,
        )
        response.raise_for_status()

        return response.json()

    async def post(
        self,
        endpoint: str,
        *,
        json: dict[str, Any],
    ) -> Any:
        response = await self._client.post(
            endpoint,
            json=json,
        )
        response.raise_for_status()

        return response.json()

    async def patch(
        self,
        endpoint: str,
        *,
        json: dict[str, Any],
    ) -> Any:
        response = await self._client.patch(
            endpoint,
            json=json,
        )
        response.raise_for_status()

        return response.json()

    async def delete(
        self,
        endpoint: str,
    ) -> None:
        response = await self._client.delete(
            endpoint,
        )
        response.raise_for_status()

    async def aclose(self) -> None:
        await self._client.aclose()
