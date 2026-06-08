from .browser_agent import BrowserAgentServiceFactory

from ....interface.services.offer_repository_agent import OfferReposiotryAgentService

from libs.core.config import TApplicationConfig

from libs.infrastructure.factories.stores.mysql import (
    MySQLEngineFactory,
    MySQLPartnerRepository,
)


class PartnerParserServiceFactory:
    @classmethod
    def create(
        cls,
        config: type[TApplicationConfig],
    ) -> ParserAgentService:

        partner_repository = MySQLPartnerRepository.create(
            engine=MySQLEngineFactory.create(
                config=config,
            ),
        )

        browser_agent = BrowserAgentServiceFactory.create(
            config=config,
        )

        return OfferReposiotryAgentService(
            partner_repository=partner_repository,
            browser_agent=browser_agent,
        )
