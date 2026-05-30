from typing import (
    Any,
    Protocol,
)


class IHTTPAdapterProtocol(Protocol):
    async def client(
        self,
        *args,
        **kwargs,
    ) -> None: ...

    async def request(
        self,
    ) -> dict[str, Any]: ...
