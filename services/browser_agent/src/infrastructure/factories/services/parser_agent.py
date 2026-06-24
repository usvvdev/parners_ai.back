from libs.core.config import TApplicationConfig

from .browser_agent import BrowserAgentServiceFactory

from ....interface.services import ParserAgentService

from libs.infrastructure.factories.api import APIClientsFactory


class ParserAgentServiceFactory:
    @staticmethod
    def create(
        config: type[TApplicationConfig],
    ) -> ParserAgentService:
        browser_agent = BrowserAgentServiceFactory.create(
            # config=config,
        )
        api_clients = APIClientsFactory.create(
            config=config,
        )
        return ParserAgentService(
            browser_agent=browser_agent,
            api_clients=api_clients,
        )
