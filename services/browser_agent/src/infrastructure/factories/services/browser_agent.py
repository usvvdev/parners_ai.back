# packages

from typing import Optional

# application dependencies

from ..clients import (
    Gemini,
    Crawler,
)

from src.interface.services import BrowserAgentService


class BrowserAgentFactory:
    @staticmethod
    def create(
        crawler: Optional[Crawler] = None,
        gemini: Optional[Gemini] = None,
    ) -> BrowserAgentService:
        return BrowserAgentService(
            crawler=crawler or Crawler(),
            gemini=gemini or Gemini(),
        )
