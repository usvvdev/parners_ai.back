from .base import PaginatedResponse
from .link import FetchLinks
from .offer import FetchOffer
from .partner import (
    FetchPartner,
    FetchPartners,
    InsertPartner,
    UpdatePartner,
)
from .utm_source import (
    FetchUTMSource,
    InsertUTMSource,
)
from .offer_position import InsertOfferPosition
from .scan import (
    ScannedOffer,
    PartnerResult,
)

__all__ = [
    "PaginatedResponse",
    "FetchLinks",
    "FetchOffer",
    "FetchPartner",
    "FetchPartners",
    "InsertPartner",
    "UpdatePartner",
    "FetchUTMSource",
    "InsertUTMSource",
    "InsertOfferPosition",
    "ScannedOffer",
    "PartnerResult",
]
