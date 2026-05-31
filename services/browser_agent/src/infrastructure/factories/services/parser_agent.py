from .browser_agent import BrowserAgentServiceFactory

from src.interface.services.parser_agent import ParserAgentService

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

        return ParserAgentService(
            partner_repository=partner_repository,
            browser_agent=browser_agent,
        )
