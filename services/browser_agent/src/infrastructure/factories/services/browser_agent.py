# packages

from typing import Optional

# application dependencies

from ...clients import (
    Gemini,
    Crawler,
)

from libs.core.config import TApplicationConfig

from src.interface.services import BrowserAgentService


class BrowserAgentServiceFactory:
    @staticmethod
    def create(
        crawler: Optional[Crawler] = None,
        gemini: Optional[Gemini] = None,
        *,
        config: type[TApplicationConfig],
    ) -> BrowserAgentService:
        return BrowserAgentService(
            crawler=crawler or Crawler(),
            gemini=gemini
            or Gemini(
                config=config,
            ),
        )
