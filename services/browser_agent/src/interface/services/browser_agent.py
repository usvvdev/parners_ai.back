# application dependencies

from ...domain.protocols.agent import (
    ICrawlerProtocol,
    IOCRProtocol,
)

from ...domain.types._types import PartnerResult


class BrowserAgentService:
    def __init__(
        self,
        crawler: ICrawlerProtocol,
        analyzer: IOCRProtocol,
    ) -> None:
        self._crawler = crawler
        self._analyzer = analyzer

    async def parse(
        self,
        *,
        link: str,
        target_offers: list[str],
    ) -> PartnerResult:
        page = await self._crawler.crawl(
            link=link,
        )

        result = await self._analyzer.analyze(
            showcase_url=link,
            target_offers=target_offers,
            html=page.html or "",
            markdown=page.markdown or "",
        )

        result.link = link

        return result

    async def capture_offer_redirect_url(
        self,
        url: str,
    ) -> str:
        if not url:
            return url

        return await self._crawler.navigate_and_capture_url(
            link=url,
        )
