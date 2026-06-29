from libs.core.config import TApplicationConfig

from .browser_agent import BrowserAgentServiceFactory

from ....interface.services import (
    NotificationService,
    ParserAgentService,
)

from libs.infrastructure.factories.api import APIClientsFactory


class ParserAgentServiceFactory:
    @staticmethod
    def create(
        config: type[TApplicationConfig],
    ) -> ParserAgentService:
        browser_agent = BrowserAgentServiceFactory.create()
        api_clients = APIClientsFactory.create(
            config=config,
        )
        notification_service = NotificationService(
            telegram_options=config.telegram_options,
            proxy_url=config.proxy_url,
        )

        return ParserAgentService(
            browser_agent=browser_agent,
            api_clients=api_clients,
            notification_service=notification_service,
        )
