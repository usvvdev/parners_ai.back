from .browser_agent import BrowserAgentService

from src.domain.types.partner_result import PartnerResult

from libs.infrastructure.stores.mysql.repositories import PartnerRepository


class ParserAgentService:
    def __init__(
        self,
        partner_repository: PartnerRepository,
        browser_agent: BrowserAgentService,
    ):
        self._partner_repository = partner_repository
        self._browser_agent = browser_agent

    async def execute(
        self,
    ) -> list[PartnerResult]:
        partners = await self._partner_repository.fetch()

        if not partners:
            return []

        results = []

        for partner in partners:
            result = await self._browser_agent.parse(
                link=partner.link,
                target_offers=[partner.offers],
            )

            results.append(result)

        return results
