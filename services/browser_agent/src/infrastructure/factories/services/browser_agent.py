# application dependencies

from ...clients import (
    Gemini,
    Crawler,
)

from libs.core.config import TApplicationConfig

from ....interface.services import BrowserAgentService


class BrowserAgentServiceFactory:
    @staticmethod
    def create(
        config: type[TApplicationConfig],
    ) -> BrowserAgentService:
        return BrowserAgentService(
            crawler=Crawler(),
            gemini=Gemini(
                config=config,
            ),
        )
