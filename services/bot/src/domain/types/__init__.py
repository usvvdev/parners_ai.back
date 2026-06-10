from .offer import OfferSummary

from .link import (
    LinkSummary,
    LinkDetail,
)

from .partner import (
    Partner,
    PartnerDetail,
)

from .pagination import PaginatedResponse

__all__: list[str] = [
    "OfferSummary",
    "LinkSummary",
    "LinkDetail",
    "Partner",
    "PartnerDetail",
    "PaginatedResponse",
]
