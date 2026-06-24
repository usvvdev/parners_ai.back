from typing import (
    Any,
    Protocol,
)


class IHTTPClientProtocol(Protocol):
    async def get(
        self,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any: ...

    async def post(
        self,
        endpoint: str,
        *,
        json: dict[str, Any],
    ) -> Any: ...

    async def patch(
        self,
        endpoint: str,
        *,
        json: dict[str, Any],
    ) -> Any: ...

    async def delete(
        self,
        endpoint: str,
    ) -> None: ...
