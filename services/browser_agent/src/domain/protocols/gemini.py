# packages

from typing import (
    Any,
    Protocol,
)


class IGeminiProtocol(Protocol):
    async def analyze(
        self,
        *,
        screenshot: str,
        markdown: str,
        target_offers: list[str],
    ) -> Any:
        raise NotImplementedError
