# application dependencies

from pydantic import ConfigDict

from ...clients.ai.crawler import Crawler
from ...clients.ai.gemini import Gemini
from ..base import APIClients

from ....interface.services import (
    BrowserAgentService,
    ParserAgentService,
)

from libs.core.config import TApplicationConfig
from libs.domain.types._types.common import BaseModelType


class AgentServices(BaseModelType):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=True,
    )

    parser: ParserAgentService


class AgentServicesFactory:
    @staticmethod
    def create(
        config: type[TApplicationConfig],
        clients: APIClients,
    ) -> AgentServices:
        browser_agent = BrowserAgentService(
            crawler=Crawler(),
            gemini=Gemini(config=config),
        )

        parser = ParserAgentService(
            browser_agent=browser_agent,
            link_client=clients.link,
            offer_client=clients.offer,
            partner_client=clients.partner,
            utm_source_client=clients.utm_source,
            offer_position_client=clients.offer_position,
        )

        return AgentServices(
            parser=parser,
        )
