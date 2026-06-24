from .start import start_router

from .main import main_router

from .partner import partner_router

from .link import link_router

from .offer import offer_router

__all__: list[str] = [
    "start_router",
    "main_router",
    "partner_router",
    "link_router",
    "offer_router",
]
