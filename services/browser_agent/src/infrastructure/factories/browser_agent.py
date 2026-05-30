from ..clients import (
    Gemini,
    Crawler,
)

from .gemini import GeminiFactory

from src.interface.services import BrowserAgentService


class BrowserAgentFactory:
    @staticmethod
    def create(
        crawler: Crawler = Crawler(),
        gemini: Gemini = GeminiFactory.create(),
    ) -> BrowserAgentService:
        return BrowserAgentService(
            crawler=crawler,
            gemini=gemini,
        )
