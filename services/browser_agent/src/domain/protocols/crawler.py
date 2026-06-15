# packages

from typing import Protocol

from crawl4ai import CrawlResult


class ICrawlerProtocol(Protocol):
    async def crawl(
        self,
        *,
        link: str,
    ) -> CrawlResult:
        raise NotImplementedError

    async def navigate_and_capture_url(
        self,
        *,
        link: str,
    ) -> str:
        raise NotImplementedError
