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
    FiltersLink,
)

from .utm_source import (
    FetchUTMSource,
    FetchUTMSources,
    InsertUTMSource,
    UpdateUTMSource,
)

from .offer_position import (
    FetchOfferPosition,
    InsertOfferPosition,
    FiltersOfferPosition,
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
    "FiltersLink",
    "FetchUTMSource",
    "FetchUTMSources",
    "InsertUTMSource",
    "UpdateUTMSource",
    "FetchOfferPosition",
    "InsertOfferPosition",
    "FiltersOfferPosition",
]
