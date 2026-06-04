from .offer import (
    InsertOffer,
    FetchOffer,
    FetchOffers,
)

from .partner import (
    FetchPartner,
    FetchPartners,
    InsertPartner,
)

from .link import (
    FetchLink,
    FetchLinks,
    InsertLink,
)

__all__: list[str] = [
    "InsertOffer",
    "FetchOffer",
    "FetchOffers",
    "FetchPartner",
    "FetchPartners",
    "InsertPartner",
    "FetchLink",
    "FetchLinks",
    "InsertLink",
]
