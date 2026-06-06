from .browser_agent import BrowserAgentService

from ...domain.types.partner_result import PartnerResult

from libs.infrastructure.stores.mysql.repositories import LinkRepository


class ParserAgentService:
    def __init__(
        self,
        link_repository: LinkRepository,
        browser_agent: BrowserAgentService,
    ):
        self._partner_repository = link_repository
        self._browser_agent = browser_agent

    async def execute(
        self,
    ) -> list[PartnerResult]:
        links = await self._partner_repository.fetch()

        if not links:
            return []

        results = []

        for link in links:
            result = await self._browser_agent.parse(
                link=link.link,
                target_offers=[offer.title for offer in partner.offers],
            )

            results.append(result)

        return results
