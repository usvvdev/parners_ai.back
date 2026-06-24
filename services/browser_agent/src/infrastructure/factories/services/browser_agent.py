from ...clients import (
    CrawlerAgent,
    OCRAgent,
)

from libs.core.config import TApplicationConfig

from ....interface.services import BrowserAgentService


class BrowserAgentServiceFactory:
    @staticmethod
    def create() -> BrowserAgentService:
        crawler = CrawlerAgent(
            viewport_width=1920,
            viewport_height=4000,
        )

        return BrowserAgentService(
            analyzer=OCRAgent(
                crawler=crawler,
            ),
            crawler=crawler,
        )
