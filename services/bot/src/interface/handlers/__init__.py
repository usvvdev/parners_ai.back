from .start import router as start_router

from .partner import router as partner_router

from .link import router as link_router

from .offer import router as offer_router

from .main import router as main_router

__all__: list[str] = [
    "start_router",
    "partner_router",
    "link_router",
    "offer_router",
    "main_router",
]
