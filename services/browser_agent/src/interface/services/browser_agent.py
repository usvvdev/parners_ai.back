# application dependencies

from ...domain.protocols import (
    ICrawlerProtocol,
    IGeminiProtocol,
)
from ...domain.types._types import PartnerResult


class BrowserAgentService:
    def __init__(
        self,
        crawler: ICrawlerProtocol,
        gemini: IGeminiProtocol,
    ) -> None:
        self._crawler = crawler
        self._gemini = gemini

    async def parse(
        self,
        *,
        link: str,
        target_offers: list[str],
    ) -> PartnerResult:
        page = await self._crawler.crawl(
            link=link,
        )

        result = await self._gemini.analyze(
            screenshot=page.screenshot,
            markdown=page.markdown,
            target_offers=target_offers,
        )

        result.link = link

        return result
