# packages

from typing import Any, Protocol


class IOCRProtocol(Protocol):
    async def analyze(
        self,
        *,
        showcase_url: str,
        target_offers: list[str],
        html: str = "",
        markdown: str = "",
        screenshot: str = "",
    ) -> Any:
        raise NotImplementedError
