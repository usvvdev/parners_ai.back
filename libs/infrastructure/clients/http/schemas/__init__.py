from .link import (
    FetchLink,
    FetchLinks,
    InsertLink,
    UpdateLink,
)

from .offer import (
    FetchOffer,
    FetchOffers,
    InsertOffer,
    UpdateOffer,
)

from .partner import (
    FetchPartner,
    FetchPartners,
    InsertPartner,
    UpdatePartner,
)

from .utm_source import (
    FetchUTMSource,
    FetchUTMSources,
    InsertUTMSource,
)

from .offer_position import InsertOfferPosition

__all__: list[str] = [
    "FetchLink",
    "FetchLinks",
    "InsertLink",
    "UpdateLink",
    "FetchOffer",
    "FetchOffers",
    "InsertOffer",
    "UpdateOffer",
    "InsertOfferPosition",
    "FetchPartner",
    "FetchPartners",
    "InsertPartner",
    "UpdatePartner",
    "FetchUTMSource",
    "FetchUTMSources",
    "InsertUTMSource",
]
