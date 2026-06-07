from .offer import (
    InsertOffer,
    FetchOffer,
    FetchOffers,
    UpdateOffer,
)

from .partner import (
    FetchPartner,
    FetchPartners,
    InsertPartner,
    UpdatePartner,
)

from .link import (
    FetchLink,
    FetchLinks,
    InsertLink,
    UpdateLink,
)

__all__: list[str] = [
    "InsertOffer",
    "UpdateOffer",
    "FetchOffer",
    "FetchOffers",
    "FetchPartner",
    "FetchPartners",
    "InsertPartner",
    "UpdatePartner",
    "FetchLink",
    "FetchLinks",
    "InsertLink",
    "UpdateLink",
]
