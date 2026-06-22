from ...clients import (
    CrawlerAgent,
    GeminiAgent,
)

from libs.core.config import TApplicationConfig

from ....interface.services import BrowserAgentService


class BrowserAgentServiceFactory:
    @staticmethod
    def create(
        config: type[TApplicationConfig],
    ) -> BrowserAgentService:
        return BrowserAgentService(
            gemini=GeminiAgent(
                config=config,
            ),
            crawler=CrawlerAgent(
                viewport_width=1920,
                viewport_height=4000,
            ),
        )
