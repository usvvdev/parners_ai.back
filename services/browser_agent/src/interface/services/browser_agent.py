from ...domain.protocols import (
    ICrawlerProtocol,
    IGeminiProtocol,
)

from ...domain.types import PartnerResult

from libs.infrastructure.stores.clickhouse.repositories import OfferPositionRepository


class BrowserAgentService:
    def __init__(
        self,
        *,
        crawler: ICrawlerProtocol,
        gemini: IGeminiProtocol,
        offer_position_repository: OfferPositionRepository,
    ) -> None:
        self._crawler = crawler
        self._gemini = gemini
        self._offer_position_repository = offer_position_repository

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
