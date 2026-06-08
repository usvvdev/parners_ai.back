from .services.browser_agent import BrowserAgentServiceFactory

from .services.offer_repository_agent import PartnerParserServiceFactory

__all__: list[str] = [
    "BrowserAgentServiceFactory",
    "PartnerParserServiceFactory",
]
