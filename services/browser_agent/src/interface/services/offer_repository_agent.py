# application depencies

from .browser_agent import BrowserAgentService

from ...domain.types.partner_result import PartnerResult

from libs.infrastructure.stores.mysql.repositories import (
    LinkRepository,
    OfferRepository,
    PartnerRepository,
)


class OfferReposiotryAgentService:
    def __init__(
        self,
        link_repository: LinkRepository,
        offer_repository: OfferRepository,
        partner_repository: PartnerRepository,
        browser_agent: BrowserAgentService,
    ):
        self._link_repository = link_repository
        self._offer_repository = offer_repository
        self._partner_repository = partner_repository
        self._browser_agent = browser_agent

    async def execute(
        self,
    ) -> list[PartnerResult]:
        links = await self._link_repository.fetch_many()

        if not links:
            return []

        offers = await self._offer_repository.fetch_many()

        default_offers = [offer.title for offer in offers]

        return [
            await self._browser_agent.parse(
                link=link.link,
                target_offers=[o.title for o in link.offers] or default_offers,
            )
            for link in links
        ]
