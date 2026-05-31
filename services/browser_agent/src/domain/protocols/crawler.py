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
